from celery import shared_task
from django.core.mail import send_mail
from .models import Orden


@shared_task
def orden_creada(orden_id):
    """
    Tarea para enviar un email cuando se crea una orden
    """
    orden = Orden.objects.get(id=orden_id)
    subject = f'Orden nr. {orden.id}'
    message = f'Estimado {orden.nombre},\n\n' \
        f'Has realizado una orden satisfactoriamente.' \
        f'El ID de tu orden es: {orden.id}.'
    mail_sent = send_mail(subject,
                message,
                'egoallin@gmail.com',
                [orden.email])
    return mail_sent