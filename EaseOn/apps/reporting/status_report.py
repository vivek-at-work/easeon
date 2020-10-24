from .db_query import REPORT_SQL_MAPPING, STATUS_REPORT
from .base_report import Report, validate_date


class StatusReport(Report):
    def __init__(self, file_name):
        self.type = STATUS_REPORT
        db_query = REPORT_SQL_MAPPING[self.type]
        super().__init__(STATUS_REPORT, db_query, file_name)

    def filter_by_centre(self, centre):
        if centre:
            self.db_query = (
                "{} where tickets_ticket.organization_id = {}".format(
                    REPORT_SQL_MAPPING[self.type], str(centre)
                )
            )

    def filter_by_date(self, date):
        if date and validate_date(date):
            self.db_query = "{0} where tickets_ticket.created_at >= CAST('{1}' AS DATE) AND tickets_ticket.created_at < (CAST('{1}' AS DATE) + CAST('1 day' AS INTERVAL))".format(
                REPORT_SQL_MAPPING[self.type], date
            )

    def filter_by_centre_and_date(self, centre, start_date, end_date):
        if (
            centre
            and start_date
            and validate_date(start_date)
            and validate_date(end_date)
        ):
            db_query = self.filter_by_centre(centre)
            self.db_query = (
                self.db_query
                + " AND tickets_ticket.created_at >= CAST('{1}' AS DATE) AND tickets_ticket.created_at < (CAST('{2}' AS DATE) + CAST('1 day' AS INTERVAL))".format(
                    REPORT_SQL_MAPPING[self.type], start_date, end_date
                )
            )
