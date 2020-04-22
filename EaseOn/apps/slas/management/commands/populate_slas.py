# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from slas.models import SLA, Term

SLAS = []
TICKET_SLA = {
    'sla_type': 'TICKET_SLA',
    'name': 'Default Ticket SLA',
    'terms': [
        {
            'statement': 'Apple or Apple Authorized Service centre (AASP) will not be responsible for any damage to the product that occurs during the repair process that is a result of any unauthorized modifications or repairs or replacements not performed by Apple or an AASP. If damage results, Apple will seek your authorization for any additional costs for completing the service even if the product is covered by warranty or an AppleCare service plan. If you decline authorization, Apple may return your product unprepared in the damaged condition without any responsibility.',
            'heading': None,
        },
        {
            'statement': 'No responsibility for data backup, screen guards, wear and tear. And no warranty for liquid/physical damages, and unauthorised modifications found in the device.Estimation given may vary at the time of approval for processing the part or during servicing of the product. Equipment is accepted subject to the terms and conditions mentioned overleaf..',
            'heading': None,
        },
    ],
}
DELIVERY_SLA = {
    'sla_type': 'DELIVERY_SLA',
    'name': 'Default Delivery SLA',
    'terms': [
        {
            'statement': 'Apple or Apple Authorized Service centre (AASP) will not be responsible for any damage to the product that occurs during the repair process that is a result of any unauthorized modifications or repairs or replacements not performed by Apple or an AASP. If damage results, Apple will seek your authorization for any additional costs for completing the service even if the product is covered by warranty or an AppleCare service plan. If you decline authorization, Apple may return your product unprepared in the damaged condition without any responsibility.',
            'heading': None,
        },
        {
            'statement': 'No responsibility for data backup, screen guards, wear and tear. And no warranty for liquid/physical damages, and unauthorised modifications found in the device.Estimation given may vary at the time of approval for processing the part or during servicing of the product. Equipment is accepted subject to the terms and conditions mentioned overleaf..',
            'heading': None,
        },
    ],
}

PHONE_LOAN_AGREEMENT = {
    'sla_type': 'PHONE_LOAN_AGREEMENT',
    'name': 'Default PHONE LOAN AGREEMENT SLA',
    'terms': [
        {
            'statement': "You acknowledge receipt of the Loaner Phone listed below which at Service Provider’s discretion may be new or refurbished, and agree to return it to Service Provider (i) no more than fourteen (14) days from the date Service Provider notifies you that your repaired Customer Phone is ready for pickup or (ii) upon Service Provider’s written request to do so (each, a 'Return Date'):.From the date on which you receive the Loaner Phone through the Return Date, title to the Loaner Phone shall at all times remain vested in Service Provider.",
            'heading': 'Loaner Phone',
        },
        {
            'statement': ' Service Provider may require a valid credit card number prior to providing a Loaner Phone. An authorization, in the amount of the Replacement Value listed in the table below will be placed on your credit card. In the event that you fail to return the Loaner Phone to Service Provider by the Return Date your credit card will be charged the Replacement Value. After confirmation that any and all charges have been paid, the authorization on your credit card will expire.',
            'heading': 'In Case of Failure/Damage to Return Loaner Phone',
        },
        {
            'statement': 'If you have a circumstance that prevents you from picking up your repaired Customer Phone on or before the Return Date, you may submit a request to Service Provider for an extension of five (5) days beyond the standard fourteen (14) day return period. You may submit a request for the extension by contacting Service Provider at the location where the Loaner Phone was provided. Upon approval of the five (5) day extension, the extended date will become your Return Date for purposes of these terms, and you will be required to return the Loaner Phone by that extended Return Date. All of the terms set forth in this agreement will apply to that extended Return Date.',
            'heading': 'Extended Return Date',
        },
        {
            'statement': ' Where Service Provider determines that replacement of the Customer Phone is required (e.g., where repair is not possible or entails disproportionate costs): (i) you will return the Loaner Phone to Service Provider and collect the Replacement Phone, for which all original terms of sale that applied to the Customer iPhone, including the remainder of any warranty terms still in effect will apply; (ii) provided that you return the Loaner Phone, you will obtain full rights of ownership in the Replacement Phone, and (iii) Service Provider will obtain full rights of ownership in the Customer Phone and may use or dispose of the Customer Phone as Service Provider sees fit.',
            'heading': 'Replacement',
        },
        {
            'statement': 'You must take reasonable and prudent precautions to protect the Loaner Phone against damage, loss, or abuse while in your care, custody, and control. If the Loaner Phone is lost, stolen or damaged, you must notify Service Provider immediately. Only Service Provider may service the Loaner Phone. You may be held responsible for repair or replacement costs if the Loaner Phone is lost, damaged, or stolen while on loan.',
            'heading': 'Safeguarding',
        },
        {
            'statement': "Use. The Loaner Phone is to be used solely by you while your iPhone is being serviced by Service Provider ('Service Period'). You must not use the Loaner Phone for any unlawful purpose. Only software with valid licenses should be loaded on the Loaner Phone.",
            'heading': 'Permitted Use',
        },
        {
            'statement': ' You acknowledge that before returning the Loaner Phone, you are responsible for erasing all files, including personal and/or confidential files and data, created by you. Therefore, should you wish to retain any files you created, you should backup your files using iTunes or iCloud so that the files can later be transferred to your repaired Customer Phone. You are responsible for removing and storing any such files prior to returning the Loaner iPhone. Service Provider or Apple is not responsible nor liable for any files or data remaining on, or erased from the Loaner Phone, following its return.',
            'heading': 'Delete Your Files Upon Return of Loaner Phone',
        },
        {
            'statement': ' You acknowledge that all software provided with the Loaner Phone is licensed specifically to this Loaner Phone and you will not remove it. You also agree not to copy or otherwise reproduce, reverse engineer, disassemble or decompile any software, the equipment, or components provided with the Loaner Phone.',
            'heading': 'Installed Software',
        },
        {
            'statement': 'Service Provider will not be liable for any: (i) consequential; (ii) incidental; (iii) indirect; or (iv) direct damages; arising out of these terms or the use of the Loaner Phone, including without limitation any losses of or affecting your personal property, software or data. THIS LIMITATION IS NOT INTENDED TO EXCLUDE ANY LIABILITY FOR DEATH OR PERSONAL INJURY, FRAUD, FRAUDULENT MISREPRESENTATION OR ANY LIABILITY THAT ARISES UNDER CONSUMER LAW WHICH CANNOT BE EXCLUDED.',
            'heading': 'Service Provider Liability',
        },
        {
            'statement': 'This Agreement shall be governed by and construed in accordance with the laws of the country in which the Loaner Phone is provided. The undersigned has read and understands this Agreement and hereby acknowledges receipt of a copy.',
            'heading': 'Governing Law',
        },
    ],
}

SLAS.append(TICKET_SLA)
SLAS.append(DELIVERY_SLA)
SLAS.append(PHONE_LOAN_AGREEMENT)


class Command(BaseCommand):
    help = 'Populate Initial SLAS'

    def handle(self, *args, **options):
        SLA.objects.all().delete()
        for l in SLAS:
            sla, created = SLA.objects.get_or_create(
                sla_type=l['sla_type'],
                name=l['name'],
                is_default=True,
                created_by=get_user_model().objects.first(),
            )
            for t in l['terms']:
                t, created = Term.objects.get_or_create(
                    statement=t['statement'],
                    heading=t['heading'],
                    created_by=get_user_model().objects.first(),
                )
                t.sla.add(sla)
