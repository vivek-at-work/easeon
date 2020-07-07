STATUS_REPORT = 'STATUS_REPORT'
LOANER_RECORD_REPORT = 'LOANER_RECORD_REPORT'
ORDER_LINE_REPORT= 'ORDER_LINE_REPORT'
SQL_STATUS_REPORT = """
SELECT tickets_ticket.reference_number , 
devices_device.serial_number,
devices_device.alternate_device_id,
devices_device.product_name,
customers_customer.first_name,
customers_customer.last_name,
customers_customer.email,
customers_customer.contact_number,
tickets_ticket.status,
tickets_ticket.repair_type,
tickets_ticket.coverage_type,
tickets_ticket.issue_reported_by_customer,
tickets_ticket.expected_service_cost,
tickets_ticket.expected_hardware_cost,
tickets_ticket.expected_delivery_time
from tickets_ticket JOIN devices_device ON tickets_ticket.device_id = devices_device.id 
join customers_customer ON tickets_ticket.customer_id  = customers_customer.id
"""
SQL_LOANER_RECORD_REPORT ="""SELECT tickets_ticket.reference_number, organizations_organization.code , inventory_loanerinventoryitem.serial_number, inventory_loanerinventoryitem.part_number,
inventory_loanerinventoryitem.po_number,inventory_loanerinventoryitem.description,
tickets_loanerrecord.created_at,
tickets_loanerrecord.returned_on,tickets_loanerrecord.is_lost,tickets_loanerrecord.penalty
from organizations_organization JOIN inventory_loanerinventoryitem 
ON organizations_organization.id = inventory_loanerinventoryitem.organization_id
JOIN tickets_loanerrecord ON inventory_loanerinventoryitem.id = tickets_loanerrecord.inventory_item_id  
JOIN tickets_ticket ON tickets_loanerrecord.ticket_id  = tickets_ticket .id"""


SQL_ORDER_LINE_REPORT = """SELECT tickets_ticket.reference_number, organizations_organization.code ,
inventory_repairinventoryitem.serial_number , inventory_repairinventoryitem.part_number,
inventory_repairinventoryitem.po_number,inventory_repairinventoryitem.description,
tickets_orderline.created_at,tickets_orderline.kbb_serial_number,tickets_orderline.kbb_serial_number,
tickets_orderline.quantity,tickets_orderline.amount
from organizations_organization JOIN inventory_repairinventoryitem 
ON organizations_organization.id = inventory_repairinventoryitem.organization_id
JOIN tickets_orderline ON  tickets_orderline.inventory_item_id = inventory_repairinventoryitem.id
JOIN tickets_ticket ON tickets_orderline.ticket_id  = tickets_ticket .id
"""

REPORT_SQL_MAPPING = {
    STATUS_REPORT:SQL_STATUS_REPORT,
    LOANER_RECORD_REPORT:SQL_LOANER_RECORD_REPORT,
    ORDER_LINE_REPORT:SQL_ORDER_LINE_REPORT
}