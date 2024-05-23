from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orden.models import Orden


@shared_task
def pago_completado(orden_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    orden = Orden.objects.get(id=orden_id)
    # create invoice e-mail
    subject = f'My Shop - Invoice no. {orden.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                        message,
                        'admin@myshop.com',
                        [orden.email])
    # generar PDF
    html = render_to_string('ordenes/orden/pdf.html', {'orden': orden})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                        stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{orden.id}.pdf',
                out.getvalue(),
                'application/pdf')
    # send e-mail
    email.send()