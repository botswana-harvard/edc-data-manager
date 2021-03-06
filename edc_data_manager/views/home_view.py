from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..view_mixins import UserDetailsCheckViewMixin


class HomeView(
        EdcBaseViewMixin, UserDetailsCheckViewMixin,
        NavbarViewMixin, TemplateView):

    template_name = 'edc_data_manager/home.html'
    navbar_name = 'edc_data_manager'
    navbar_selected_item = 'edc_data_manager'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
