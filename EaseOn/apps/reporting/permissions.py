# -*- coding: utf-8 -*-
from core.permissions.superuser import PRIVILEGED, SUPER_USER, IsOperatorOrSuperUser
from .db_query import DELIVERY_REPORT, STATUS_REPORT,LOANER_RECORD_REPORT,ORDER_LINE_REPORT

REPORT_TYPE_RIGHTS_MAPPING={
DELIVERY_REPORT:'daily_status_report_download',
STATUS_REPORT:'daily_status_report_download',
ORDER_LINE_REPORT:'daily_status_report_download',
LOANER_RECORD_REPORT:'daily_status_report_download'
}

class HasReportDownloadPermissions(IsOperatorOrSuperUser):
    """
    Allows Only Manager or super user to update only to Super users.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == SUPER_USER or request.user.role == PRIVILEGED:
            return True

        if (
            view.action in ["download"]
            and request.user
            and request.user.is_authenticated
        ):
            condition_1 = request.user == obj.organization.manager
            criteria = {
                    'organization':obj.organization,
                    REPORT_TYPE_RIGHTS_MAPPING[obj.report_type]:True
                }
            condition_2 = request.user.locations.filter(**criteria).exists()
            return condition_1 or condition_2
        return True
