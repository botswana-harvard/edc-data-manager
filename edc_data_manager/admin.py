from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple

from .admin_site import edc_data_manager_admin
from .forms import DataActionItemForm
from .models import DataActionItem
from .modeladmin_mixin import ExportActionMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin,
                      ExportActionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(DataActionItem, site=edc_data_manager_admin)
class DataActionItemAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DataActionItemForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'subject',
                'assigned',
                'status',
                'action_priority',
                'comment',
                'issue_number',
                'action_date',)}),
        audit_fieldset_tuple
    )

    radio_fields = {
        "action_priority": admin.VERTICAL,
        "status": admin.VERTICAL}

    readonly_fields = ('issue_number', 'action_date')

    list_display = [
        'created', 'subject_identifier', 'assigned', 'issue_number',
        'status', 'user_created', 'user_modified', 'modified']

    list_filter = [
        'status', 'created', 'user_created', 'modified', 'user_modified']

    search_fields = ('subject_identifier',)
