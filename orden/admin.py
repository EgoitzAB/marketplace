import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Orden, OrdenItem


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'adjunto; nombre_archivo={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
            field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.nombre)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Exportar a CSV'


class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    raw_id_fields = ['producto']


# def orden_pago(obj):
#     url = obj.get_stripe_url()
#     if obj.stripe_id:
#         html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
#         return mark_safe(html)
#     return ''
# orden_pago.short_description = 'Stripe payment'

# def order_detail(obj):
#     url = reverse('orders:admin_order_detail', args=[obj.id])
#     return mark_safe(f'<a href="{url}">View</a>')


# def order_pdf(obj):
#     url = reverse('orders:admin_order_pdf', args=[obj.id])
#     return mark_safe(f'<a href="{url}">PDF</a>')
# order_pdf.short_description = 'Invoice'


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'first_name', 'last_name', 'email',
#                     'address', 'postal_code', 'city', 'paid',
#                     order_payment, 'created', 'updated',
#                     order_detail, order_pdf]
#     list_filter = ['paid', 'created', 'updated']
#     inlines = [OrderItemInline]
#     actions = [export_to_csv]
