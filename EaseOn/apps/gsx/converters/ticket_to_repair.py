

from .get_code_state_name import get_code_state_name

class TicketToRepairConverter:
    def __init__(self, ticket):
        self.ticket = ticket
        self.data = {}

    def get_customer(self):
        customer = self.ticket.customer
        customerInfo = {
        'firstName': customer.first_name,
        'lastName': customer.last_name,
        'primaryPhone': customer.contact_number,
        'emailAddress': customer.email,
        'address': [
            {
            'city': customer.city,
            'countryCode': "IND",
            'postalCode': customer.pin_code,
            'stateCode': get_code_state_name(customer.state),
            'line2': customer.address_line_2[0:59] if customer.address_line_2 is not None else None,
            'line1': customer.address_line_1[0:59],
            },
        ]
        }
        return customerInfo

    def get_device(self):
        device = self.ticket.device
        return {
        "id": device.serial_number
      }

    def get_customer_intake_note(self):
        return {
            'type': "CUSTOMER_INTAKE_NOTES",
            'content': self.ticket.issue_reported_by_customer
        }

    def get_technician_note(self):
        if hasattr(self.ticket, 'delivery') and self.ticket.delivery:
            return {
                'type': "TECHNICIAN",
                'content': self.ticket.delivery.action_taken
            }
        return {
                'type': "TECHNICIAN",
                'content': None
            }

    def get_loaners(self):
        if hasattr(self.ticket, 'loaner_records') and self.ticket.loaner_records:
            records =  self.ticket.loaner_records.all()
            results =  []
            for r in records:
                inventory_item =  r.inventory_item
                results.append({
                    'partUsed':inventory_item.part_number,
                    'fromConsignedStock':True,
                    'partNumber': inventory_item.part_number,
                    'device': {
                             "id": inventory_item.serial_number
                        }
                    })
            return results

    def get_repair_flags(self):
        return {
            'requestReviewByApple':	self.ticket.request_review_by_apple,
            'markComplete': self.ticket.mark_complete
        }

    def get_parts(self):
        if hasattr(self.ticket, 'order_lines') and self.ticket.order_lines:
            records =  self.ticket.order_lines.all()
            results =  []
            for r in records:
                inventory_item =  r.inventory_item
                consignment_type = inventory_item.consignment_type
                results.append({
                    'number':inventory_item.part_number,
                    'partUsed':inventory_item.part_number,
                    'kgbDeviceDetail':{'id':inventory_item.serial_number},
                    'fromConsignedStock':r.from_consigned_stock,
                    'pricingOption': r.pricing_option,
                    'coverageOption':r.coverage_option
                    })
            return results

    def get_component_issues(self):
        component_issues = self.ticket.device.component_issues.all()
        current_ord = 1
        out = []
        for com in component_issues:
            data = {
                'componentCode': com.component_code,
                'reproducibility':com.reproducibility,
                'priority':com.priority,
                'type':'CUST',
                'issueCode':com.issue_code,
                'order':current_ord
            }
            out.append(data)
            data = {
            'componentCode': com.component_code,
            'reproducibility':com.reproducibility,
            'priority':com.priority,
            'type':'TECH',
            'issueCode':com.issue_code,
            'order':current_ord
            }
            out.append(data)
            current_ord = current_ord + 1
        return out


    def convert(self):
        self.data = {
            'notes':[
                self.get_customer_intake_note(),
            ],
            "repairClassification":self.ticket.repair_classification,
            "repairType":self.ticket.device.gsx_repair_type,
            "serviceNonRepairType":self.ticket.device.gsx_service_non_repair_type,
            "coverageOption":self.ticket.gsx_coverage_option,
            "unitReceivedDateTime":self.ticket.created_at,
            'loanerStockUnavailable':self.ticket.loaner_stock_unavailable,
            "reservationId":self.ticket.customer.token_number,
            "referenceNumber":self.ticket.reference_number,
            "purchaseOrderNumber":self.ticket.reference_number,
            'addressCosmeticDamage':self.ticket.device.address_cosmetic_changes,
            'componentIssues':self.get_component_issues(),
            "techId":self.ticket.created_by.gsx_technician_id,
            "device":self.get_device(),
            'customer':self.get_customer(),
        }
        if self.ticket.device.gsx_repair_type in ['MINS', 'MINC']:
            data['boxRequired'] = self.ticket.box_required
        t_note = self.get_technician_note()
        if t_note and t_note['content']:
            self.data['notes'].append(t_note)
        loaners = self.get_loaners()
        if loaners:
            self.data['loaners'] = loaners
        if self.ticket.device.gsx_repair_type in ['CIN', 'CINR']:
            parts = self.get_parts()
            if parts:
                self.data['parts'] = parts



class SVNRTicketToRepairConverter(TicketToRepairConverter):
    def __init__(self, ticket):
        super(SVNRTicketToRepairConverter, self).__init__(ticket)


    def convert(self):
        self.data = {
            'notes':[
                self.get_customer_intake_note(),
            ],
            "repairClassification":self.ticket.repair_classification,
            "repairType":self.ticket.device.gsx_repair_type,
            "serviceNonRepairType":self.ticket.device.gsx_service_non_repair_type,
            "coverageOption":self.ticket.gsx_coverage_option,
            "unitReceivedDateTime":self.ticket.created_at,
            'loanerStockUnavailable':self.ticket.loaner_stock_unavailable,
            "referenceNumber":self.ticket.reference_number,
            "purchaseOrderNumber":self.ticket.reference_number,
            'addressCosmeticDamage':self.ticket.device.address_cosmetic_changes,
            'componentIssues':self.get_component_issues(),
            "techId":self.ticket.created_by.gsx_technician_id,
            "device":self.get_device(),
            'customer':self.get_customer(),
        }
        t_note = self.get_technician_note()
        if t_note and t_note['content']:
            self.data['notes'].append(t_note)
        else:
            self.data['meta']={'messages':['Add Delivery Info to create a repair']}


def get_convertor_class(gsx_repair_type):
    d = {
        'SVNR': SVNRTicketToRepairConverter
    }
    return d.get(gsx_repair_type,None)


