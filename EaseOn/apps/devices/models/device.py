# -*- coding: utf-8 -*-
import re
from core import utils

from gsx.core import DEVICE_DIAGNOSTICS_INELIGIBLE, GSXRequest
from core.models import BaseModel
from core.utils import send_mail, time_by_adding_business_days
from django.conf import settings
from django.db import models
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from devices.exceptions import DeviceDetailsExceptions
from devices.validators import (
    validate_restricted_device,
    validate_identifier,
    gsx_validate,
)


class Device(BaseModel):
    serial_number = models.CharField(
        null=True,
        max_length=20,
        validators=[validate_identifier, validate_restricted_device],
    )
    alternate_device_id = models.CharField(
        null=True,
        max_length=20,
        validators=[validate_identifier, validate_restricted_device],
    )
    product_name = models.CharField(null=True, max_length=100)
    configuration = models.CharField(null=True, max_length=100)

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def _set_device_identifier(self, number):
        if gsx_validate(number, 'alternateDeviceId'):
            self.alternate_device_id = number
        else:
            self.serial_number = number

    def _get_device_identifier(self):
        if self.alternate_device_id:
            return self.alternate_device_id
        if self.serial_number:
            return self.serial_number
        return 'NA'

    @property
    def identifier(self):
        return self._get_device_identifier()

    @identifier.setter
    def identifier(self, number):
        self._set_device_identifier(number)

    @property
    def is_exempted_device(self):
        return (
            self.alternate_device_id in settings.EXEMPTED_DEVICE
            or self.serial_number in settings.EXEMPTED_DEVICE
        )

    @property
    def open_tickets(self):
        Ticket = apps.get_model(utils.get_ticket_model())
        return Ticket.objects.filter(
            device__serial_number=self.serial_number
        ).open()

    def get_parts(self, gsx_username, authtoken, **kwargs):
        payload = {
            'devices': [{'id': self.identifier}],
            'componentIssues': [
                {
                    'componentCode': '26095B',
                    'reproducibility': 'A',
                    'priority': 1,
                    'type': 'TECH',
                    'issueCode': 'IP146',
                    'order': 1,
                }
            ],
        }
        req = GSXRequest('parts', 'summary', gsx_username, authtoken)
        response = req.post(payload=payload)
        return response

    def fetch_diagnosis_lookup(self, gsx_username, authtoken, **kwargs):
        """
        The Fetch Diagnostic Details API allows
        technicians to get the diagnostic test
        details of the unit under test.
        This API retrieves all diagnostics run
        on the device in the 12 months.
        """
        if settings.GSX_DUMMY_RESPONSE:
            return {
                'diagnostics': [
                    {
                        'context': {
                            'diagnosticEventNumber': '3516819986',
                            'diagnosticEndTimeStamp': '2019-10-23T09:04:50.329Z',
                            'channelId': 'GSX',
                            'diagnosticStartTimeStamp': '2019-10-23T09:04:50Z',
                            'diagnosticEventEndResult': 'WARNING',
                            'captureId': '3516819986',
                            'serialNumber': 'FCGT24E5HFM2',
                            'suite': 'Mobile Resource Inspector',
                            'systemId': 'AST2_IOS',
                            'soldTo': '0000547988',
                            'productId': '1511',
                            'shipTo': '0001026647',
                            'localizedDiagnosticEventEndResult': 'WARNING',
                            'isCustomerReportEligible': False,
                            'accountId': '0000547988',
                        },
                        'testResults': [
                            {
                                'testName': 'Diagnostic Version Check',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '8166',
                                'testType': 'Software',
                                'moduleName': 'Software',
                            },
                            {
                                'testName': 'Restore from Backup History',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '3745',
                                'testType': 'Services',
                                'moduleName': 'Services',
                            },
                            {
                                'testName': 'Backup History',
                                'testStatus': 'WARNING',
                                'testStatusCode': '-101',
                                'testId': '3738',
                                'testType': 'Services',
                                'testMessage': 'This device has not been backed up in the last two weeks.',
                                'moduleName': 'Services',
                            },
                            {
                                'testName': 'Temperature History',
                                'testStatus': 'WARNING',
                                'testStatusCode': '-901',
                                'testId': '3744',
                                'testType': 'Sensors',
                                'moduleName': 'Sensors',
                                'moduleLocation': 'thermal',
                            },
                            {
                                'testName': 'Accelerometer Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4005',
                                'testType': 'Accelerometer',
                                'moduleName': 'Accelerometer',
                            },
                            {
                                'testName': 'Ambient Light Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4003',
                                'testType': 'ALS',
                                'moduleName': 'ALS',
                            },
                            {
                                'testName': 'Barometer Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4004',
                                'testType': 'Barometer',
                                'moduleName': 'Barometer',
                            },
                            {
                                'testName': 'Bluetooth Scan Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4008',
                                'testType': 'Bluetooth',
                                'moduleName': 'Bluetooth',
                            },
                            {
                                'testName': 'Camera Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4009',
                                'testType': 'Camera',
                                'moduleName': 'Camera',
                                'moduleLocation': 'Front',
                            },
                            {
                                'testName': 'Camera Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4009',
                                'testType': 'Camera',
                                'moduleName': 'Camera',
                                'moduleLocation': 'Rear',
                            },
                            {
                                'testName': 'Compass Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4006',
                                'testType': 'Compass',
                                'moduleName': 'Compass',
                            },
                            {
                                'testName': 'Presence Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2749',
                                'testType': 'Baseband',
                                'moduleName': 'Cellular',
                            },
                            {
                                'testName': 'Gyro Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4007',
                                'testType': 'Gyro',
                                'moduleName': 'Gyro',
                            },
                            {
                                'testName': 'Presence Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2749',
                                'testType': 'WiFi',
                                'moduleName': 'Wi-Fi',
                            },
                            {
                                'testName': 'Presence Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2749',
                                'testType': 'TouchID',
                                'moduleName': 'Touch ID',
                            },
                            {
                                'testName': 'Apple Pay Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4002',
                                'testType': 'ApplePay',
                                'moduleName': 'ApplePay',
                            },
                            {
                                'testName': 'Version Test',
                                'testStatus': 'WARNING',
                                'testStatusCode': '-101',
                                'testId': '3733',
                                'testType': 'Software',
                                'testMessage': 'The system software is not up to date. Updates are available for the device.',
                                'moduleName': 'Software',
                            },
                            {
                                'testName': 'Health Check',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2389',
                                'testType': 'Battery',
                                'testMessage': 'Testing completed and no issues were found on this device. View Details for more information.',
                                'moduleName': 'Battery',
                            },
                            {
                                'testName': 'App Crash History',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '3734',
                                'testType': 'Software',
                                'moduleName': 'Software',
                            },
                        ],
                    },
                    {
                        'context': {
                            'diagnosticEventNumber': '3508171042',
                            'diagnosticEndTimeStamp': '2019-10-21T05:42:02.172Z',
                            'channelId': 'GSX',
                            'diagnosticStartTimeStamp': '2019-10-21T05:42:02Z',
                            'diagnosticEventEndResult': 'WARNING',
                            'captureId': '3508171042',
                            'serialNumber': 'FCGT24E5HFM2',
                            'suite': 'Mobile Resource Inspector',
                            'systemId': 'AST2_IOS',
                            'soldTo': '0000547988',
                            'productId': '1511',
                            'shipTo': '0001026647',
                            'localizedDiagnosticEventEndResult': 'WARNING',
                            'isCustomerReportEligible': False,
                            'accountId': '0000547988',
                        },
                        'testResults': [
                            {
                                'testName': 'Diagnostic Version Check',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '8166',
                                'testType': 'Software',
                                'moduleName': 'Software',
                            },
                            {
                                'testName': 'Restore from Backup History',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '3745',
                                'testType': 'Services',
                                'moduleName': 'Services',
                            },
                            {
                                'testName': 'Backup History',
                                'testStatus': 'WARNING',
                                'testStatusCode': '-101',
                                'testId': '3738',
                                'testType': 'Services',
                                'testMessage': 'This device has not been backed up in the last two weeks.',
                                'moduleName': 'Services',
                            },
                            {
                                'testName': 'Temperature History',
                                'testStatus': 'WARNING',
                                'testStatusCode': '-901',
                                'testId': '3744',
                                'testType': 'Sensors',
                                'moduleName': 'Sensors',
                                'moduleLocation': 'thermal',
                            },
                            {
                                'testName': 'Accelerometer Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4005',
                                'testType': 'Accelerometer',
                                'moduleName': 'Accelerometer',
                            },
                            {
                                'testName': 'Ambient Light Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4003',
                                'testType': 'ALS',
                                'moduleName': 'ALS',
                            },
                            {
                                'testName': 'Barometer Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4004',
                                'testType': 'Barometer',
                                'moduleName': 'Barometer',
                            },
                            {
                                'testName': 'Bluetooth Scan Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4008',
                                'testType': 'Bluetooth',
                                'moduleName': 'Bluetooth',
                            },
                            {
                                'testName': 'Camera Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4009',
                                'testType': 'Camera',
                                'moduleName': 'Camera',
                                'moduleLocation': 'Front',
                            },
                            {
                                'testName': 'Camera Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4009',
                                'testType': 'Camera',
                                'moduleName': 'Camera',
                                'moduleLocation': 'Rear',
                            },
                            {
                                'testName': 'Compass Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4006',
                                'testType': 'Compass',
                                'moduleName': 'Compass',
                            },
                            {
                                'testName': 'Presence Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2749',
                                'testType': 'Baseband',
                                'moduleName': 'Cellular',
                            },
                            {
                                'testName': 'Gyro Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4007',
                                'testType': 'Gyro',
                                'moduleName': 'Gyro',
                            },
                            {
                                'testName': 'Presence Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2749',
                                'testType': 'TouchID',
                                'moduleName': 'Touch ID',
                            },
                            {
                                'testName': 'Presence Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2749',
                                'testType': 'WiFi',
                                'moduleName': 'Wi-Fi',
                            },
                            {
                                'testName': 'Apple Pay Sensor Test',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '4002',
                                'testType': 'ApplePay',
                                'moduleName': 'ApplePay',
                            },
                            {
                                'testName': 'Version Test',
                                'testStatus': 'WARNING',
                                'testStatusCode': '-101',
                                'testId': '3733',
                                'testType': 'Software',
                                'testMessage': 'The system software is not up to date. Updates are available for the device.',
                                'moduleName': 'Software',
                            },
                            {
                                'testName': 'Health Check',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '2389',
                                'testType': 'Battery',
                                'testMessage': 'Testing completed and no issues were found on this device. View Details for more information.',
                                'moduleName': 'Battery',
                            },
                            {
                                'testName': 'App Crash History',
                                'testStatus': 'PASSED',
                                'testStatusCode': '0',
                                'testId': '3734',
                                'testType': 'Software',
                                'moduleName': 'Software',
                            },
                        ],
                    },
                ]
            }
        device = {'id': self.identifier}
        req = GSXRequest('diagnostics', 'lookup', gsx_username, authtoken)
        response = req.post(device=device)
        return response

    def fetch_diagnosis_status(self, gsx_username, authtoken, **kwargs):
        device = {'id': self.identifier}
        req = GSXRequest('diagnostics', 'status', gsx_username, authtoken)
        response = req.post(device=device)
        return response

    def fetch_diagnosis_console_url(
        self, eventNumber, gsx_username, authtoken
    ):
        """The Fetch Diagnostic Customer Report
        URL API allows users to retrieve the
        customer report associated with the
        diagnostic event number.
        GSX UI login is required in order
        to access this report.
        The Customer Report is only available for the MRI diagnostic suite."""
        req = GSXRequest(
            'diagnostics', 'customer-report-url', gsx_username, authtoken
        )
        response = req.post(eventNumber=eventNumber)
        return response

    def run_diagnosis_suite(self, suiteId, gsx_username, authtoken):
        if settings.GSX_DUMMY_RESPONSE:
            return {'diagnosticsInitiated': True}

        diagnostics = {'suiteId': suiteId}
        device = {'id': self.identifier}
        req = GSXRequest(
            'diagnostics', 'initiate-test', gsx_username, authtoken
        )
        response = req.post(diagnostics=diagnostics, device=device)
        return response

    def get_diagnostic_suites(self, gsx_username, authtoken, **kwargs):
        if settings.GSX_DUMMY_RESPONSE:
            return {
                'suiteDetails': [
                    {
                        'suiteId': '151104',
                        'suiteName': 'Mobile Resource Inspector',
                        'timeEstimate': {'minimum': '1', 'maximum': '1'},
                    },
                    {
                        'suiteId': '151102',
                        'suiteName': 'Battery Usage',
                        'timeEstimate': {'minimum': '5', 'maximum': '10'},
                    },
                    {
                        'suiteId': '151103',
                        'suiteName': 'Call Performance',
                        'timeEstimate': {'minimum': '1', 'maximum': '1'},
                    },
                ]
            }
        req = GSXRequest('diagnostics', 'suites', gsx_username, authtoken)
        response = req.get(deviceId=self.identifier)
        if (
            'errors' in response
            and response['errors'][0]['code'] == DEVICE_DIAGNOSTICS_INELIGIBLE
        ):
            return []
        return response

    def get_warranty(self, gsx_username, authtoken, **kwargs):
        print('584')
        # {'errorId': '557cd1d8-2dcd-40f4-b27d-bfe89eccac43', 'errors': [{'code': 'DEVICE_INFORMATION_INVALID', 'message': 'Invalid Device Information.'}]}
        if settings.GSX_DUMMY_RESPONSE:
            return {
                'device': {
                    'identifiers': {
                        'serial': 'FCGT24E5HFM2',
                        'imei': '359223073482536',
                        'meid': '35922307348253',
                    },
                    'productDescription': 'iPhone 6s Plus Updated Qwerty1234',
                    'loaner': False,
                    'activationDetails': {
                        'carrierName': 'IDEA',
                        'lastRestoreDate': '2019-09-15T20:36:05Z',
                        'firstActivationDate': '2017-05-26T10:29:57Z',
                        'unlocked': True,
                        'unlockDate': '2017-05-26T10:29:57Z',
                        'productVersion': '12.4.1',
                        'initialActivationPolicyID': '10',
                        'initialActivationPolicyDetails': 'Unlock.',
                        'appliedActivationPolicyID': '10',
                        'appliedActivationDetails': 'Unlock.',
                        'nextTetherPolicyID': '10',
                        'nextTetherPolicyDetails': 'Unlock.',
                        'productDescription': 'IPHONE 6S PLUS SPACE GRAY 32GB-HIN',
                        'lastUnbrickOsBuild': '16G102',
                    },
                    'productLine': '500040',
                    'configCode': 'HFM2',
                    'configDescription': 'IPHONE 6S PLUS,NB30,32GB,GRAY',
                    'soldToName': 'BRIGHTSTAR TELECOMMUNICATIONS(I)LTD',
                    'warrantyInfo': {
                        'warrantyStatusCode': 'OO',
                        'warrantyStatusDescription': 'Out Of Warranty (No Coverage)',
                        'daysRemaining': 0,
                        'purchaseDate': '2017-05-26T00:00:00Z',
                        'purchaseCountry': 'IND',
                        'registrationDate': '2017-05-26T00:00:00Z',
                        'onsiteCoverage': False,
                        'laborCovered': False,
                        'limitedWarranty': False,
                        'partCovered': False,
                        'personalized': False,
                    },
                }
            }
        req = GSXRequest(
            'repair',
            'product/details?activationDetails=true',
            gsx_username,
            authtoken,
        )
        device = {'id': self.identifier}
        received_on = time_by_adding_business_days(0).isoformat()
        response = req.post(unitReceivedDateTime=received_on, device=device)
        if 'errorId' in response:
            raise DeviceDetailsExceptions(
                response['errors'][0]['message'], response
            )
        return response

    def get_repair_eligibility(self, gsx_username, authtoken, **kwargs):
        req = GSXRequest('repair', 'eligibility', gsx_username, authtoken)
        device = {'id': self.identifier}
        response = req.post(device=device)
        return response

    def get_component_issue(self, gsx_username, authtoken, **kwargs):
        req = GSXRequest(
            'repair', 'product/componentissue', gsx_username, authtoken
        )
        device = {'id': self.identifier}
        response = req.post(device=device)
        return response

    def get_repair_questions(self, gsx_username, authtoken, **kwargs):
        req = GSXRequest('repair', 'questions', gsx_username, authtoken)
        payload = {
            'repairType': 'CIN',
            'componentIssues': [
                {
                    'componentCode': 'IPSAFE',
                    'priority': 1,
                    'type': 'TECH',
                    'issueCode': 'IPSAFE1',
                    'order': 1,
                }
            ],
            'device': {'id': self.identifier},
        }
        response = req.post(payload=payload)
        return response

    def get_previous_gsx_repairs(self, gsx_username, authtoken, **kwargs):
        """
        /repair/summary
        The Repair Summary Lookup API returns a
        subset of repair information for
        up to 50 repairs matching the search criteria.
        For full details use the Repair Details Lookup API.
        """
        req = GSXRequest('repair', 'summary', gsx_username, authtoken)
        device = {'id': self.identifier}
        response = req.post(device=device)
        return response

    def __str__(self):
        return self.identifier


# @receiver(post_save, sender=Device)
# def restricted_device_update(sender, instance, *args, **kwargs):
#     if instance.validate_restricted_device():
#         template = settings.EMAIL_TEMPLATES.get('action')
#         details = """We have found that a restricted
#                      device with identifier {0}
#                      has been accessed by the
#                      user {1} you may contact him
#                      on {2}.""".format(
#             instance.identifier,
#             instance.created_by.full_name,
#             instance.created_by.contact_number,
#         )
#         summary = '''Urgent !! A Restricted
#             Device {0} has been accessed .'''.format(
#             instance.identifier
#         )
#         context = {'summary': summary, 'detail': details}
#         subject = """Urgent !! A Restricted Device {0} has been accessed .""".format(
#             instance.identifier
#         )

#         context['receiver_short_name'] = settings.ADMIN_NAME
#         send_mail(subject, template, [settings.ADMIN_EMAIL], **context)
