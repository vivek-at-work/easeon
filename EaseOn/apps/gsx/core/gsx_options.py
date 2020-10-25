# -*- coding: utf-8 -*-
CONSUMER_LAW_OPTIONS = (
    ("RFD", "Refund"),
    ("RPL", "Replace"),
    ("SVC", "Service"),
    ("OPT_IN", "Customer has opted in for Consumer Law coverage"),
    ("OPT_OUT", "Customer has opted out of Consumer Law coverage"),
)

REPAIR_TYPES = (
    ("SVNR", "Service Non-Repair"),
    ("CRBR", "Carry-In Return Before Replace"),
    ("DION", "Onsite Service Direct"),
    ("MINC", "Mail-In Return to Customer"),
    ("CINR", "Carry-In Non-Replenishment"),
    ("INON", "Onsite Service Indirect"),
    ("CIN", "Carry-In"),
    ("WUMS", "Whole Unit Mail-In Return to Service Location"),
    ("WUMC", "Whole Unit Mail-In Return to Customer"),
    ("OSR", "Onsite Service Facilitated"),
    ("OSCR", "Onsite Service Pickup"),
)

REPAIR_CLASSIFICATIONS = (
    ("SINGLE", "Single submission - Customer requests one repair"),
    ("BULK", "Bulk submission - Customer requests multiple repairs"),
    ("NEEDS_EXTRA_UNDERSTANDING", "Needs extra understanding"),
)

REPAIR_NOTES_TYPE = (
    ("CUSTOMER_INTAKE_NOTES", "Customer intake notes"),
    ("TECHNICIAN", "Technician notes"),
    ("HOLD_REVIEW", "Notes for review"),
    ("REVIEW_RESULT", "Notes indicating results for review hold"),
    ("REP_STS", "Repair status notes"),
    ("RC_NOTE", "Repair Center notes"),
)


REPRODUCIBILITY = (
    ("A", "Not Applicable"),
    ("B", "Continuous"),
    ("D", "Fails After Warm Up"),
    ("E", "Environmental"),
    ("F", "Configuration: Peripheral"),
    ("G", "Damaged"),
    ("H", "Screening Request"),
)

RETURN_STATUSES = (
    ("DOA", "Dead on arrival"),
    ("CTS", "Convert to stock"),
    ("GPR", "Good part return"),
    ("TOW", "Transfer to OOW"),
    ("SDOA", "Stock dead on arrival"),
)

COVERAGE_OPTIONS = (
    ("BATTERY", "Billable battery repair"),
    ("DISPLAY", "Billable display repair"),
    ("VMI_YELLOW", "VMI Yellow, service price"),
    ("APPLECARE_PLUS", "AppleCare+ covered incident"),
    ("VMI_RED", "VMI Red, full price"),
    ("VMI_GREEN", "VMI Green"),
)

LOANER_RETURN_DISPOSITIONS = (
    ("LRFR", "	Recycle Loaner - Place back in stock"),
    ("LVFN", "	Component Check Failed - Abandoned"),
    ("LEXP", "	Loaner Expired"),
    ("LABN", "	Repair Abandoned - No charge, iPhone return"),
    ("LRTN", "	Return Loaner - No damage, no charge"),
    ("LABS", "	Non-Repairable Damage - Return, no charge"),
    ("LRDD", "	Return Loaner - Display damage"),
    ("DOA", "	Loaner Dead on Arrival - Return, no charge"),
    ("LOST", "	Loaner Lost - Charge, no return"),
    ("LVFU", "	Component Check Failed - Charge"),
    ("LABE", "	Return Loaner - Repairable Damage"),
)

REPAIR_OUTCOME_REASONS = (
    ("HOLD", "Denotes that repair is created and is put on hold"),
    ("STOP", "Denotes that repair cannot be created"),
    ("MESSAGE", "Denotes that repair is created"),
    ("REPAIR_TYPE", "Eligible repair types"),
    ("WARNING", "Additional coverage details"),
)

KGB_MISMATCH_REASONS = (("RS", "Return from Stock"), ("OT", "Other"))

GOOD_PART_RETURN_REASONS = (
    ("PNN", "Part Not Needed"),
    ("CRO", "Customer Refused Order"),
    ("WRP", "Added Wrong Part"),
    ("CNC", "Tried to Cancel Order"),
    ("DUP", "Duplicated Part"),
)

GOOD_PART_RETURN_TYPES = (("UOP", "Unopened box"), ("DIA", "Diagnostic part"))

SERVICE_NON_REPAIR_TYPES = (
    ("NTF", "No Trouble Found"),
    ("SRC", "Screening"),
    ("LUA", "Loaner Unavailable"),
)

LOANER_STATUSES = (
    ("AL", "Available"),
    ("OL", "On Loan"),
    ("DO", "Dead on Arrival"),
    ("UN", "Unavailable"),
)
