from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from orden.models import Orden
import requests
from carrito.context_processors import carrito
import logging
from secrets import compare_digest
from allauth.account.decorators import verified_email_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone


def prueba_order(request):
    context = {}
    return render(request, 'pago/payindex.html', {'context': context})

def get_paygreen_jwt_token():
    """ Obtener el token de pago """
    url = "https://sb-api.paygreen.fr/auth/authentication/sh_1f13f081e35c460fbec63e876ea184e3/secret-key"
    headers = {"Authorization": "sk_b88a2138936d43839ac81686f7bbc2ea"}

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        jwt_token = response.json().get("data", {}).get("token")
        return jwt_token
    else:
        return None

def create_buyer(jwt, order):
    buyer_url = "https://sb-api.paygreen.fr/payment/buyers"
    buyer_data = {
                "billing_address": {
                "city": str(order.ciudad),
                "country": str(order.estado),
                "line1": str(order.direccion),
                "postal_code": str(order.codigo_postal),
                "state": str(order.provincia)
                },
                "reference": f"{order.nombre} {order.apellido} / {order.email} {order.id}",
                "first_name": str(order.nombre),
                "last_name": str(order.apellido),
                "email": str(order.email),
                "phone_number": str(order.telefono),
                }

    headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {jwt}"
            }

    buyer_response = requests.post(buyer_url, json=buyer_data, headers=headers)
    if buyer_response.status_code == 200:
        response_data = buyer_response.json()
        buy_id = response_data.get('data', {}).get('id')
        return buy_id
    else:
        return HttpResponse("Failed to create a buyer on PayGreen", status=buyer_response.status_code)

@verified_email_required
@login_required
def realizar_compra(request):
    """Crear la orden y manejar la redirección a la página de pago y la vuelta"""
    orden_id = request.session.get('orden_id')
    if not orden_id:
        return redirect('compra:carrito')

    try:
        orden = Orden.objects.get(id=orden_id, usuario=request.user)
    except Orden.DoesNotExist:
        return redirect('compra:carrito')

    # Verificar y reservar stock
    try:
        with transaction.atomic():
            # Reservar stock
            for item in orden.items.select_for_update():
                producto = item.producto
                cantidad = item.cantidad
                if producto.stock >= cantidad:
                    producto.stock -= cantidad
                    producto.save()
                else:
                    logging.error("Stock insuficiente para el producto %s", producto.id)
                    return render(request, 'pago/error.html', {'error_message': f"Stock insuficiente para el producto {producto.nombre}"})

            # Stock reservado, proceder con el pago
            jwt_token = get_paygreen_jwt_token()
            if not jwt_token:
                raise ValueError("Error al obtener el token JWT de PayGreen")

            buy_id = create_buyer(jwt_token, orden)
            payload = {
                "auto_capture": True,
                "buyer": buy_id,
                "currency": "eur",
                "merchant_initiated": False,
                "mode": "instant",
                "partial_allowed": False,
                "amount": int(orden.total * 100),  # Convertir a céntimos
                "description": f"Orden número {orden.id} LRVCBD",
                "integration_mode": "hosted_fields",
                "reference": f"r{orden.id}",
                "return_url": request.build_absolute_uri(reverse('pago:confirmacion', args=[orden.id])),
                "cancel_url": request.build_absolute_uri(reverse('pago:cancelacion', args=[orden.id])),
                "shop_id": "sh_1f13f081e35c460fbec63e876ea184e3"
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {jwt_token}"
            }
            paygreen_url = "https://sb-api.paygreen.fr/payment/payment-orders"
            response = requests.post(paygreen_url, json=payload, headers=headers)

            if response.status_code == 200:
                created_order = response.json()
                hosted_payment_url = created_order['data']['hosted_payment_url']
                request.session.set_expiry(60)
                # Pago exitoso, stock ya ha sido reducido
                return redirect(hosted_payment_url)
            else:
                raise ValueError(f"Error al crear la compra en PayGreen: {response.text}")

    except ValueError as e:
        # Registra el error
        logging.error(str(e))
        return render(request, 'pago/error.html', {'error_message': str(e)})
    except requests.exceptions.RequestException as e:
        # Registra el error en el sistema de registro de Django
        logging.error("Error al realizar la solicitud a PayGreen: %s", str(e))
        return render(request, 'pago/error.html', {'error_message': str(e)})

@login_required
def confirmacion_compra(request, compra_id):
    compra = Orden.objects.get(id=compra_id)
    return render(request, 'pago/confirmacion.html', {'compra': compra})

@login_required
def cancelacion_compra(request, compra_id):
    compra = Orden.objects.get(id=compra_id)
    return render(request, 'pago/cancelacion.html', {'compra': compra})
