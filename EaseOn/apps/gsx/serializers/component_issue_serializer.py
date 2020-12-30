# -*- coding: utf-8 -*-
import copy

from core.utils import is_in_dev_mode, time_by_adding_business_days
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer

dummy_response = {
    "componentIssues": [
        {
            "componentCode": "OSSUK",
            "componentDescription": "Unknown OSS Symptom",
            "issues": [
                {"code": "WOS", "description": "Unknown OSS Symptom"},
                {"code": "FOS", "description": "Unknown OSS Symptom"},
                {"code": "EOS", "description": "Unknown OSS Symptom"},
                {"code": "B9Y", "description": "Unknown OSS Symptom"},
            ],
        },
        {
            "componentCode": "26114A",
            "componentDescription": "Camera/Flash",
            "issues": [
                {"code": "IP326", "description": "Camera - App Only"},
                {"code": "IP327A", "description": "Camera - Front (Hardware)"},
                {"code": "IP328", "description": "LED Flash"},
                {"code": "IP497", "description": "Rear Camera - No Preview"},
                {"code": "IP498", "description": "Rear Camera - Image/Video Quality"},
                {"code": "IP499", "description": "Rear Camera - Foreign Material"},
            ],
        },
        {
            "componentCode": "26100A",
            "componentDescription": "Sensors",
            "issues": [
                {"code": "IP286A", "description": "Accelerometer/Gyro/Barometer"},
                {"code": "IP060", "description": "Proximity Sensor"},
                {"code": "IP287", "description": "Ambient Light Sensor (ALS)"},
                {"code": "IP457", "description": "Apple Pay Update Alert"},
            ],
        },
        {
            "componentCode": "26094",
            "componentDescription": "Bluetooth/Wi-Fi",
            "issues": [
                {"code": "IP022", "description": "Bluetooth"},
                {"code": "IP025", "description": "Wi-Fi"},
            ],
        },
        {
            "componentCode": "26104",
            "componentDescription": "System-wide Issues",
            "issues": [
                {"code": "IP314", "description": "Capacity/Low disk space"},
                {"code": "IP316", "description": "Power On - Device Unresponsive"},
                {"code": "IP315", "description": "Device running slowly"},
                {"code": "IP111", "description": "Unexpected Restart / Shutdown"},
                {"code": "IP218", "description": "Temperature / Accessory Alert"},
                {"code": "IP254", "description": "Device not seen in computer"},
            ],
        },
        {
            "componentCode": "26093A",
            "componentDescription": "Buttons and Switches",
            "issues": [
                {"code": "IP050", "description": "Side / Sleep-Wake Button"},
                {"code": "IP048", "description": "Home button"},
                {"code": "IP051", "description": "Volume Buttons"},
                {"code": "IP253", "description": "Switch - Ringer/Silent"},
            ],
        },
        {
            "componentCode": "26110",
            "componentDescription": "Customer Sensory Issues",
            "issues": [
                {"code": "IP305", "description": "Temperature perception: Unit"},
                {"code": "IP306", "description": "Temperature perception: AC Adapter"},
                {"code": "IP350", "description": "Unexpected noise (not an alert)"},
                {"code": "IP351", "description": "Unexpected Alert Noise"},
            ],
        },
        {
            "componentCode": "26117",
            "componentDescription": "Vibration/Haptics",
            "issues": [
                {"code": "IP373", "description": "Weak Vibration/Weak Haptic (Taptic)"},
                {"code": "IP374", "description": "No Vibration/No Haptic (Taptic)"},
            ],
        },
        {
            "componentCode": "26118",
            "componentDescription": "Backup/Migrate/Update/Restore",
            "issues": [
                {"code": "IP261", "description": "iOS SW Update / iOS SW Restore"},
                {"code": "IP415", "description": "Erase all content and settings"},
                {"code": "IP484", "description": "iPhone migration"},
                {"code": "IP416", "description": "Backup device"},
                {"code": "IP299", "description": "Restore backup"},
                {"code": "MS1011", "description": "Migrate from Android"},
            ],
        },
        {
            "componentCode": "26121",
            "componentDescription": "Face ID / Touch ID",
            "issues": [
                {
                    "code": "IP450",
                    "description": "Unlock-Authenticate Face ID /Touch ID",
                },
                {"code": "IP448", "description": "Unable to Set up Face ID / Touch ID"},
            ],
        },
        {
            "componentCode": "26099",
            "componentDescription": "Power",
            "issues": [
                {"code": "IP115", "description": "Will Not Power On/Wired Charging"},
                {"code": "PD22-09", "description": "REP AC Wall Plug Adapter"},
                {"code": "IP044", "description": "Battery Life/Performance"},
                {"code": "PD38-04", "description": "REP AC 3-PRONG WALL PLUG ADAPTER"},
                {"code": "IP492", "description": "REP 6s/6s+ No Power On"},
                {
                    "code": "IP493",
                    "description": "REP 6s/6s+ No Power On (multi issue)",
                },
            ],
        },
        {
            "componentCode": "26092A",
            "componentDescription": "Apple Apps",
            "issues": [
                {"code": "IP426", "description": "Files"},
                {"code": "IP428", "description": "iTunes U"},
                {"code": "IP430", "description": "Support App"},
                {"code": "IP432", "description": "Airport Utility"},
                {"code": "IP423", "description": "Home"},
                {"code": "IP410", "description": "Apple Watch"},
                {"code": "IP402", "description": "Tips"},
                {"code": "IP400", "description": "Health"},
                {"code": "IP250", "description": "Reminders"},
                {"code": "IP248", "description": "Messages"},
                {"code": "IP040", "description": "Weather"},
                {"code": "IP038", "description": "Stocks"},
                {"code": "IP036", "description": "Safari"},
                {"code": "IP033", "description": "Notes"},
                {"code": "IP032", "description": "Maps"},
                {"code": "IP031", "description": "Mail"},
                {"code": "IP223", "description": "FaceTime"},
                {"code": "IP026", "description": "Contacts"},
                {"code": "IP174", "description": "Compass"},
                {"code": "IP019", "description": "Calendar"},
                {"code": "IP030", "description": "Calculator"},
                {"code": "IP178", "description": "Voice Memos"},
                {"code": "IP460", "description": "Measure"},
                {"code": "IP412", "description": "Find My"},
                {"code": "IP494", "description": "Apple Research App"},
                {"code": "IP49A", "description": "Shortcuts"},
                {"code": "IP411", "description": "Fitness"},
                {"code": "IP451", "description": "Animoji/Memoji"},
                {"code": "IP500", "description": "Translate"},
                {"code": "IP021", "description": "Clock"},
            ],
        },
        {
            "componentCode": "26112B",
            "componentDescription": "Physical Damage",
            "issues": [
                {"code": "IP122", "description": "Liquid Damage"},
                {"code": "IP210", "description": "Speaker/Mic/Receiver (Damage)"},
                {"code": "IP271", "description": "Button/Switch (Damage)"},
                {"code": "IP275", "description": "Counterfeit device (suspected)"},
                {"code": "IP276", "description": "Display - Multiple cracks"},
                {"code": "IP277", "description": "Display - Single hairline crack"},
                {"code": "IP278", "description": "Dock connector on device"},
                {"code": "IP279", "description": "Enclosure - dent/scratch/crack"},
                {"code": "IP280", "description": "Enclosure - discoloration"},
                {"code": "IP282", "description": "Headphone/Headset port"},
                {"code": "IP330", "description": "Camera Lens (Damage)"},
                {"code": "IP346", "description": "Enclosure - Bubbling"},
                {"code": "IP399", "description": "Enterprise entitled replacement"},
                {"code": "B9W", "description": "Lost iPhone Reported"},
                {
                    "code": "IP380",
                    "description": "Diagnostic Fee (Singapore/Shenzhen only)",
                },
                {"code": "IP352", "description": "Enclosure - Bent"},
                {"code": "IP110", "description": "SIM tray"},
                {"code": "IP304", "description": "Swollen battery"},
                {"code": "IP329", "description": "Physical Damage During Repair"},
            ],
        },
        {
            "componentCode": "26113",
            "componentDescription": "Accessories",
            "issues": [
                {"code": "IP235", "description": "Apple Power Adapter"},
                {"code": "IP239", "description": "Apple Headset/Headphones"},
                {"code": "IP342", "description": "Apple iPhone Case"},
                {"code": "IP358", "description": "REP European 5W USB Power Adapter"},
                {"code": "IP376", "description": "Apple Lightning Accessories"},
                {"code": "IP123", "description": "3rd-Party Accessory"},
            ],
        },
        {
            "componentCode": "26101B",
            "componentDescription": "Features/Settings",
            "issues": [
                {"code": "IP433", "description": "Control Center"},
                {"code": "IP434", "description": "Multitasking / Drag&Drop"},
                {"code": "IP168", "description": "Date and Time"},
                {"code": "TV4G18", "description": "TV Provider Sign In"},
                {"code": "IP408", "description": "Night Shift"},
                {"code": "IP355", "description": "CarPlay"},
                {"code": "IP348", "description": "AirDrop"},
                {"code": "IP292", "description": "International/Region Format"},
                {"code": "IP262", "description": "Notifications/Do Not Disturb"},
                {"code": "IP231", "description": "AirPlay"},
                {"code": "IP230", "description": "AirPrint"},
                {"code": "IP197", "description": "Keyboard"},
                {"code": "IP196", "description": "Privacy/Location Services"},
                {"code": "IP177", "description": "Search"},
                {"code": "IP079", "description": "Airplane mode"},
                {"code": "IP034", "description": "Passcode Lock/Auto-Lock"},
                {"code": "IP406", "description": "App Handoff"},
                {"code": "IP259", "description": "Home Screen/Lock Screen"},
                {"code": "IP471", "description": "Screen Time/Restrictions"},
                {"code": "IP491", "description": "Dark Mode"},
                {"code": "IP180", "description": "Siri"},
                {"code": "IP605", "description": "Exposure Notifications"},
            ],
        },
        {
            "componentCode": "26102",
            "componentDescription": "Sound",
            "issues": [
                {"code": "IP005", "description": "No Sound - Headset Connector"},
                {"code": "IP089", "description": "No sound - Mic"},
                {"code": "IP173", "description": "No sound - Receiver"},
                {"code": "IP077", "description": "No sound - Speaker"},
                {"code": "IP007", "description": "Sound quality - Headset Connector"},
                {"code": "IP092", "description": "Sound quality - Mic"},
                {"code": "IP172", "description": "Sound quality - Receiver"},
                {"code": "IP076", "description": "Sound quality - Speaker"},
                {"code": "IP293", "description": "System Sounds"},
            ],
        },
        {
            "componentCode": "26095B",
            "componentDescription": "Display",
            "issues": [
                {"code": "IP053", "description": "Brightness/Backlight Issues"},
                {"code": "IP056", "description": "Image Quality"},
                {"code": "IP058", "description": "Multi-touch"},
                {"code": "IP146", "description": "Blank White Screen-Power On"},
                {"code": "IP217", "description": "Blank Black Screen-Power On"},
                {"code": "IP256", "description": "Flickering / Flashing"},
                {"code": "IP258", "description": "Pixels / Foreign Material"},
                {"code": "IP343", "description": "Lines/Blocks/Bands"},
                {"code": "IP344", "description": "Display Produces Clicking Noise"},
                {"code": "IP345", "description": "Display Loose"},
                {"code": "IP372", "description": "3D Touch/Haptic Touch"},
            ],
        },
        {
            "componentCode": "IPSAFE",
            "componentDescription": "Safety",
            "issues": [
                {"code": "IP483", "description": "Skin Irritation"},
                {"code": "IPSAFE1", "description": "Fire"},
                {"code": "IPSAFE2", "description": "Leakage"},
                {"code": "IPSAFE3", "description": "Sharp Edges"},
                {"code": "IPSAFE4", "description": "Smoke"},
                {"code": "IPSAFE5", "description": "Spark / Shock"},
                {"code": "IPSAFE6", "description": "Unusual Heat"},
                {"code": "IPSAFE7", "description": "Unusual Smell"},
            ],
        },
        {
            "componentCode": "26122",
            "componentDescription": "Accessibility",
            "issues": [
                {"code": "IP462", "description": "Hearing"},
                {"code": "IP463", "description": "Physical & Motor"},
                {"code": "IP490", "description": "Other Accessibility Features"},
                {"code": "IP468", "description": "Vision"},
            ],
        },
        {
            "componentCode": "26097A",
            "componentDescription": "Cellular/Phone",
            "issues": [
                {"code": "IP419", "description": "Calls - VoLTE"},
                {"code": "IP405", "description": "iOS Instant Hotspot"},
                {"code": "IP404", "description": "Calls - Wi-Fi Calling"},
                {"code": "IP403", "description": "Calls - Calls on Other Devices"},
                {"code": "IP310", "description": "Activation/Sim not supported"},
                {"code": "IP309", "description": "Billing and Account"},
                {"code": "IP313", "description": "Call Forwarding/Caller ID"},
                {"code": "IP312", "description": "Signal Strength (Poor)"},
                {"code": "IP179", "description": "Personal Hotspot"},
                {"code": "IP127", "description": "No SIM"},
                {"code": "IP246", "description": "Invalid SIM"},
                {"code": "IP267", "description": "No Service/Searching"},
                {"code": "IP266", "description": "International/Roaming"},
                {"code": "IP264", "description": "Calls - Audio Quality"},
                {"code": "IP102", "description": "Voicemail"},
                {"code": "IP097", "description": "Ringer (vibration)"},
                {"code": "IP088", "description": "Calls - Receiving calls"},
                {"code": "IP087", "description": "Calls - Making calls"},
                {"code": "IP085", "description": "Calls - Dropped/Failed Call"},
                {"code": "IP458", "description": "Cellular Update Failed Alert"},
                {"code": "IP311", "description": "Cellular Data"},
                {"code": "IP445", "description": "Emergency Call/Text/SOS"},
                {"code": "IP134", "description": "Carrier Lock"},
            ],
        },
        {
            "componentCode": "26116A",
            "componentDescription": "Loaner Processing",
            "issues": [{"code": "IP485", "description": "No Trouble Found"}],
        },
        {
            "componentCode": "26123",
            "componentDescription": "Repair Issues",
            "issues": [
                {"code": "IP482", "description": "Issue Persists After Repair"},
                {"code": "IP379", "description": "Calibration Unsuccessful"},
                {"code": "IP329", "description": "Physical Damage During Repair"},
                {"code": "IP496", "description": "Failed Swollen Battery Repair"},
            ],
        },
    ]
}


class ComponentIssueSerializer(BaseGSXSerializer):
    """
    DeviceSerializer
    """

    data = serializers.JSONField()

    def create(self, validated_data):
        if is_in_dev_mode():
            return dummy_response
        req = GSXRequest(
            "repair",
            "product/componentissue",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy(self.validated_data["data"])
        response = req.post(**data)
        return response
