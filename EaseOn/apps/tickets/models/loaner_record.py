# -*- coding: utf-8 -*-
"""
Model For Loaner Item Issue.
"""

from core.models import BaseModel
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from inventory.models import LoanerInventoryItem
from organizations.models import Organization
from tickets.models import Ticket


class LoanerRecord(BaseModel):
    """
    A Loaner Record.
    """

    inventory_item = models.ForeignKey(
        LoanerInventoryItem,
        related_name='loaner_records',
        on_delete=models.DO_NOTHING,
    )
    ticket = models.ForeignKey(
        Ticket, related_name='loaner_records', on_delete=models.DO_NOTHING
    )
    returned_on = models.DateTimeField(null=True, blank=True)
    is_lost = models.NullBooleanField()
    penalty = JSONField()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['inventory_item']
        else:
            return []

    def set_penalty(self):
        self.penalty = self.inventory_item.penalty
        return self

    @property
    def is_returned(self):
        return self.returned_on is not None

    @property
    def agreement(self):
        return {
            'welcome_message': """is pleased to extend the offer of a loaner iPhone to you while service is performed on your current iPhone ("Customer Phone").
                          By taking possession of the equipment identified in section 1 (“Loaner Phone”)
                          and signing this agreement, you agree to all the terms and conditions listed below:
        """,
            'confer_notice': """From the date on which you receive the Loaner Phone through the Return Date, title to the Loaner Phone shall at all times remain vested in Service Provider.
        """,
            'consumer_law_info': """ THE BENEFITS CONFERRED BY THIS AGREEMENT ARE IN ADDITION TO ALL RIGHTS AND REMEDIES CONVEYED BY CONSUMER PROTECTION LAWS AND REGULATIONS.For information on your consumer law rights, please see <a>www.apple.com/legal/warranty/statutoryrights.html""",
            'terms': [
                {
                    'heading': 'Loaner Phone',
                    'value': 'You acknowledge receipt of the Loaner Phone listed below which at Service Provider’s discretion may be new or refurbished, and agree to return it to Service Provider (i) no more than fourteen (14) days from the date Service Provider notifies you that your repaired Customer Phone is ready for pickup or (ii) upon Service Provider’s written request to do so (each, a "Return Date"):',
                },
                {
                    'heading': 'In Case of Failure/Damage to Return Loaner Phone',
                    'value': 'Service Provider may require a valid credit card number prior to providing a Loaner Phone. An authorization, in the amount of the Replacement Value listed in the table below will be placed on your credit card. In the event that you fail to return the Loaner Phone to Service Provider by the Return Date your credit card will be charged the Replacement Value. After confirmation that any and all charges have been paid, the authorization on your credit card will expire.',
                },
                {
                    'heading': 'Extended Return Date',
                    'value': ' If you have a circumstance that prevents you from picking up your repaired Customer Phone on or before the Return Date, you may submit a request to Service Provider for an extension of five (5) days beyond the standard fourteen (14) day return period. You may submit a request for the extension by contacting Service Provider at the location where the Loaner Phone was provided. Upon approval of the five (5) day extension, the extended date will become your Return Date for purposes of these terms, and you will be required to return the Loaner Phone by that extended Return Date. All of the terms set forth in this agreement will apply to that extended Return Date.',
                },
                {
                    'heading': 'Replacement',
                    'value': ' Where Service Provider determines that replacement of the Customer Phone is required (e.g., where repair is not possible or entails disproportionate costs): (i) you will return the Loaner Phone to Service Provider and collect the Replacement Phone, for which all original terms of sale that applied to the Customer iPhone, including the remainder of any warranty terms still in effect will apply; (ii) provided that you return the Loaner Phone, you will obtain full rights of ownership in the Replacement Phone, and (iii) Service Provider will obtain full rights of ownership in the Customer Phone and may use or dispose of the Customer Phone as Service Provider sees fit.',
                },
                {
                    'heading': 'Safeguarding',
                    'value': 'You must take reasonable and prudent precautions to protect the Loaner Phone against damage, loss, or abuse while in your care, custody, and control. If the Loaner Phone is lost, stolen or damaged, you must notify Service Provider immediately. Only Service Provider may service the Loaner Phone. You may be held responsible for repair or replacement costs if the Loaner Phone is lost, damaged, or stolen while on loan',
                },
                {
                    'heading': 'Permitted Use',
                    'value': 'The Loaner Phone is to be used solely by you while your iPhone is being serviced by Service Provider ("Service Period"). You must not use the Loaner Phone for any unlawful purpose. Only software with valid licenses should be loaded on the Loaner Phone',
                },
                {
                    'heading': ' Delete Your Files Upon Return of Loaner Phone',
                    'value': ' You acknowledge that before returning the Loaner Phone, you are responsible for erasing all files, including personal and/or confidential files and data, created by you. Therefore, should you wish to retain any files you created, you should backup your files using iTunes or iCloud so that the files can later be transferred to your repaired Customer Phone. You are responsible for removing and storing any such files prior to returning the Loaner iPhone. Service Provider or Apple is not responsible nor liable for any files or data remaining on, or erased from the Loaner Phone, following its return.',
                },
                {
                    'heading': 'Installed Software',
                    'value': 'You acknowledge that all software provided with the Loaner Phone is licensed specifically to this Loaner Phone and you will not remove it. You also agree not to copy or otherwise reproduce, reverse engineer, disassemble or decompile any software, the equipment, or components provided with the Loaner Phone',
                },
                {
                    'heading': 'Service Provider Liability',
                    'value': ' Service Provider will not be liable for any: (i) consequential; (ii) incidental; (iii) indirect; or (iv) direct damages; arising out of these terms or the use of the Loaner Phone, including without limitation any losses of or affecting your personal property, software or data. THIS LIMITATION IS NOT INTENDED TO EXCLUDE ANY LIABILITY FOR DEATH OR PERSONAL INJURY, FRAUD, FRAUDULENT MISREPRESENTATION OR ANY LIABILITY THAT ARISES UNDER CONSUMER LAW WHICH CANNOT BE EXCLUDED',
                },
                {
                    'heading': 'Governing Law',
                    'value': ' This Agreement shall be governed by and construed in accordance with the laws of the country in which the Loaner Phone is provided. The undersigned has read and understands this Agreement and hereby acknowledges receipt of a copy',
                },
            ],
        }


@receiver(pre_save, sender=LoanerRecord)
def set_penalty(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.set_penalty()


@receiver(post_save, sender=LoanerRecord)
def disable_inventory_item(sender, instance, created, **kwargs):
    inventory_item = instance.inventory_item
    if created:
        inventory_item.consumed = True
        inventory_item.save()
    if instance.returned_on is not None:
        inventory_item.consumed = False
        inventory_item.save()
    if instance.is_lost:
        inventory_item.consumed = True
        inventory_item.blocked = True
        inventory_item.save()


@receiver(post_delete, sender=LoanerRecord)
def enable_inventory_item(sender, instance, *args, **kwargs):
    """ Deletes thumbnail files on `post_delete` """
    inventory_item = instance.inventory_item
    inventory_item.consumed = False
    inventory_item.save()
