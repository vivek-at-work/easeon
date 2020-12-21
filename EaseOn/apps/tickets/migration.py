for ticket in Ticket.objects.all():
    if ticket.unit_part_reports is None:
        unit_part_report = {}
        for r in ticket.device_part_reports.all()[0:14]:
            unit_part_report[r.part] = r.initial_status
        ticket.unit_part_reports=unit_part_report
        ticket.save()



for ticket in Ticket.objects.all():
    if hasattr(ticket, 'delivery')  and ticket.delivery.unit_part_reports is None:
        unit_part_report = {}
        delivery = ticket.delivery
        for r in ticket.device_part_reports.all()[0:14]:
            unit_part_report[r.part] = r.final_status
        delivery.unit_part_reports=unit_part_report
        delivery.save()