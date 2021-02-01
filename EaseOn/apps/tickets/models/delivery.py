# -*- coding: utf-8 -*-
from core.models import BaseModel
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .ticket import Ticket

User = get_user_model()
class Delivery(BaseModel):
    """A Service Delivery"""

    ticket = models.OneToOneField(
        Ticket, related_name="delivery", on_delete=models.CASCADE
    )
    actual_service_cost = models.FloatField(default=0.0)
    actual_hardware_cost = models.FloatField(default=0.0)
    device_pickup_time = models.DateTimeField(blank=True, null=True)
    actual_issue = models.CharField(max_length=1000)
    action_taken = models.CharField(max_length=1000)
    final_operating_system = models.CharField(max_length=50)
    outward_condition = models.CharField(max_length=1000)
    customer_signature = models.ImageField(
        upload_to="customer_signatures/deliveries", null=True, blank=True
    )
    delivery_done_by = models.ForeignKey(
        User, null=True, related_name="deliveries_done", on_delete=models.DO_NOTHING
    )

    unit_part_reports = JSONField(null=True)
    customer_feedback = JSONField(null=True)

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        ordering = ["-id"]

    def get_pdf(self):
        from weasyprint import CSS, HTML
        delivery = self
        html_string = render_to_string("delivery.html", {"ticket": delivery.ticket})
        html = HTML(string=html_string)
        margins = "{0}px {1} {2}px {1}".format(5, 5, ".5cm")
        content_print_layout = "@page {size: A4 portrait; margin: %s;}" % margins
        result = html.write_pdf(
            stylesheets=[
                CSS(string=content_print_layout),
                os.path.join(settings.STATIC_ROOT, "bootstrap.min.css"),
            ]
        )
        with tempfile.NamedTemporaryFile(
            delete=False, prefix=self.reference_number, suffix=".pdf"
        ) as output:
            output.write(result)
            output.flush()
            output = open(output.name, "rb")
            return output.read(), output.name


    def __unicode__(self):
        return self.ticket
