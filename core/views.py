from django.shortcuts import render
from django.views import generic


# Create your views here.
class InfoTiendaView(generic.TemplateView):
    pass
    # """
    # A view that renders the personal page.

    # Attributes:
    #     model (Model): The model associated with the view.
    #     template_name (str): The name of the template to be rendered.

    # Methods:
    #     get_context_data(**kwargs): Retrieves the context data for the view.

    # """

    # model = Secciones
    # template_name = "core/personal.html"

    # def get_context_data(self, **kwargs):
    #     """
    #     Retrieves the context data for the view.

    #     Args:
    #         **kwargs: Additional keyword arguments.

    #     Returns:
    #         dict: The context data for the view.

    #     """
    #     context = super().get_context_data(**kwargs)
    #     context['secciones'] = Secciones.objects.filter(categoria='personal').order_by('indice')
    #     context['pdfs'] = PDF.objects.all()
    #     return context


class TerminosDeUsoView(generic.TemplateView):
    template_name = 'core/terminos_de_uso.html'


class PrivacidadView(generic.TemplateView):
    template_name = 'core/privacidad.html'
