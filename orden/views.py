from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import OrdenItem, Orden
from .forms import OrdenCreateForm
from .tareas import orden_creada
from carrito.carrito import Carrito


def crear_orden(request):
    carrito = Carrito(request)
    if request.method == 'POST':
        form = OrdenCreateForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario = request.user
            orden.total = carrito.carrito_total()
            if carrito.coupon:
                orden.coupon = carrito.coupon
                orden.descuento = carrito.coupon.descuento
            orden.save()
            for item in carrito:
                OrdenItem.objects.create(orden=orden,
                                        producto=item['producto'],
                                        sku=item['sku'],
                                        precio=item['precio'],
                                        cantidad=item['cantidad'])
            # clear the cart
            carrito.limpiar()
            # launch asynchronous task
            orden_creada.delay(orden.id)
            # set the order in the session
            request.session['orden_id'] = orden.id
            # redirect for payment
            return redirect(reverse('pago:realizar_compra'))
    else:
        form = OrdenCreateForm()
    return render(request,
                'ordenes/orden/crear.html',
                {'carrito': carrito, 'form': form})


@staff_member_required
def admin_orden_detalle(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    return render(request,
                'admin/ordenes/orden/detalle.html',
                {'orden': orden})


@staff_member_required
def admin_orden_pdf(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    html = render_to_string('ordenes/orden/pdf.html',
                            {'orden': orden})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'archivo=order_{orden.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT / 'css/pdf.css')])
    return response