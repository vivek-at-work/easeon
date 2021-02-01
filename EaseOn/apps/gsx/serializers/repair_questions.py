# -*- coding: utf-8 -*-
import copy

from core.utils import is_in_dev_mode, time_by_adding_business_days
from gsx.core import GSXRequest
from rest_framework import serializers

from .base_gsx_serializer import BaseGSXSerializer
from .gsx_validate import gsx_validate

dummy_response = [
    {
        "templateId": "T603836",
        "trees": [
            {
                "questions": [
                    {
                        "optional": "false",
                        "questionPhrase": "Which best describes the customer's need for help?",
                        "answerType": "DPD",
                        "questionId": "Q64579",
                        "answers": [
                            {
                                "answerPhrase": "Display doesn't turn off when phone is placed next to the customer's ear",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "What kind of environment was the customer in?",
                                        "answerType": "DPD",
                                        "questionId": "Q100407",
                                        "answers": [
                                            {
                                                "answerPhrase": "Indoor",
                                                "answerId": "A101250",
                                            },
                                            {
                                                "answerPhrase": "Outdoor",
                                                "answerId": "A101251",
                                            },
                                            {
                                                "answerPhrase": "Other",
                                                "questions": [
                                                    {
                                                        "optional": "false",
                                                        "questionPhrase": "Please describe",
                                                        "answerType": "FFB",
                                                        "questionId": "Q64128",
                                                    }
                                                ],
                                                "answerId": "A68174",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A69393",
                            },
                            {
                                "answerPhrase": "Display doesn't turn on when removed from customer's ear",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "After completing the call, how long does the display take to turn back on?",
                                        "answerType": "DPD",
                                        "questionId": "Q65064",
                                        "answers": [
                                            {
                                                "answerPhrase": "Less than 4 seconds",
                                                "answerId": "A69396",
                                            },
                                            {
                                                "answerPhrase": "4 -10 seconds",
                                                "answerId": "A69397",
                                            },
                                            {
                                                "answerPhrase": "Greater than 10 seconds",
                                                "answerId": "A69398",
                                            },
                                            {
                                                "answerPhrase": "Does not turn on at all",
                                                "answerId": "A69399",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Does the customer have anything on or near them at the time that they think could be obstructing the device?",
                                        "answerType": "DPD",
                                        "questionId": "Q66028",
                                        "answers": [
                                            {
                                                "answerPhrase": "Yes",
                                                "answerId": "A20062",
                                            },
                                            {
                                                "answerPhrase": "No",
                                                "answerId": "A20063",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "During the call, did the customer move from a dark environment to a bright environment?",
                                        "answerType": "DPD",
                                        "questionId": "Q66027",
                                        "answers": [
                                            {
                                                "answerPhrase": "Yes",
                                                "answerId": "A20062",
                                            },
                                            {
                                                "answerPhrase": "No",
                                                "answerId": "A20063",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A69394",
                            },
                            {
                                "answerPhrase": "Display turns on during call",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "What kind of environment was the customer in?",
                                        "answerType": "DPD",
                                        "questionId": "Q100407",
                                        "answers": [
                                            {
                                                "answerPhrase": "Indoor",
                                                "answerId": "A101250",
                                            },
                                            {
                                                "answerPhrase": "Outdoor",
                                                "answerId": "A101251",
                                            },
                                            {
                                                "answerPhrase": "Other",
                                                "questions": [
                                                    {
                                                        "optional": "false",
                                                        "questionPhrase": "Please describe",
                                                        "answerType": "FFB",
                                                        "questionId": "Q64128",
                                                    }
                                                ],
                                                "answerId": "A68174",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A69395",
                            },
                            {
                                "answerPhrase": "Usage questions / No HW problem reported",
                                "answerId": "A64931",
                            },
                            {
                                "answerPhrase": "Other",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Provide a brief description:",
                                        "answerType": "FFB",
                                        "questionId": "Q63396",
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "What kind of environment was the customer in?",
                                        "answerType": "DPD",
                                        "questionId": "Q100407",
                                        "answers": [
                                            {
                                                "answerPhrase": "Indoor",
                                                "answerId": "A101250",
                                            },
                                            {
                                                "answerPhrase": "Outdoor",
                                                "answerId": "A101251",
                                            },
                                            {
                                                "answerPhrase": "Other",
                                                "questions": [
                                                    {
                                                        "optional": "false",
                                                        "questionPhrase": "Please describe",
                                                        "answerType": "FFB",
                                                        "questionId": "Q64128",
                                                    }
                                                ],
                                                "answerId": "A68174",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A20075",
                            },
                        ],
                    }
                ],
                "treeId": "TREE203927",
            }
        ],
    }
]


dummy_response = [
    {
        "templateId": "T603836",
        "trees": [
            {
                "questions": [
                    {
                        "optional": "false",
                        "questionPhrase":
                        "Which best describes the customer's need for help?",
                        "answerType": "DPD",
                        "questionId": "Q64579",
                        "answers": [
                            {
                                "answerPhrase":
                                "Display doesn't turn off when phone is placed next to the customer's ear",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase":
                                        "What kind of environment was the customer in?",
                                        "answerType": "DPD",
                                        "questionId": "Q100407",
                                        "answers": [
                                            {
                                                "answerPhrase": "Indoor",
                                                "answerId": "A101250",
                                            },
                                            {
                                                "answerPhrase": "Outdoor",
                                                "answerId": "A101251",
                                            },
                                            {
                                                "answerPhrase": "Other",
                                                "questions": [
                                                    {
                                                        "optional": "false",
                                                        "questionPhrase": "Please describe",
                                                        "answerType": "FFB",
                                                        "questionId": "Q64128",
                                                    },
                                                ],
                                                "answerId": "A68174",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A69393",
                            },
                            {
                                "answerPhrase":
                                "Display doesn't turn on when removed from customer's ear",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase":
                                        "After completing the call, how long does the display take to turn back on?",
                                        "answerType": "DPD",
                                        "questionId": "Q65064",
                                        "answers": [
                                            {
                                                "answerPhrase": "Less than 4 seconds",
                                                "answerId": "A69396",
                                            },
                                            {
                                                "answerPhrase": "4 -10 seconds",
                                                "answerId": "A69397",
                                            },
                                            {
                                                "answerPhrase": "Greater than 10 seconds",
                                                "answerId": "A69398",
                                            },
                                            {
                                                "answerPhrase": "Does not turn on at all",
                                                "answerId": "A69399",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase":
                                        "Does the customer have anything on or near them at the time that they think could be obstructing the device?",
                                        "answerType": "DPD",
                                        "questionId": "Q66028",
                                        "answers": [
                                            {
                                                "answerPhrase": "Yes",
                                                "answerId": "A20062",
                                            },
                                            {
                                                "answerPhrase": "No",
                                                "answerId": "A20063",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase":
                                        "During the call, did the customer move from a dark environment to a bright environment?",
                                        "answerType": "DPD",
                                        "questionId": "Q66027",
                                        "answers": [
                                            {
                                                "answerPhrase": "Yes",
                                                "answerId": "A20062",
                                            },
                                            {
                                                "answerPhrase": "No",
                                                "answerId": "A20063",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A69394",
                            },
                            {
                                "answerPhrase": "Display turns on during call",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase":
                                        "What kind of environment was the customer in?",
                                        "answerType": "DPD",
                                        "questionId": "Q100407",
                                        "answers": [
                                            {
                                                "answerPhrase": "Indoor",
                                                "answerId": "A101250",
                                            },
                                            {
                                                "answerPhrase": "Outdoor",
                                                "answerId": "A101251",
                                            },
                                            {
                                                "answerPhrase": "Other",
                                                "questions": [
                                                    {
                                                        "optional": "false",
                                                        "questionPhrase": "Please describe",
                                                        "answerType": "FFB",
                                                        "questionId": "Q64128",
                                                    },
                                                ],
                                                "answerId": "A68174",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A69395",
                            },
                            {
                                "answerPhrase": "Usage questions / No HW problem reported",
                                "answerId": "A64931",
                            },
                            {
                                "answerPhrase": "Other",
                                "questions": [
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Provide a brief description:",
                                        "answerType": "FFB",
                                        "questionId": "Q63396",
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase": "Issue frequency?",
                                        "answerType": "DPD",
                                        "questionId": "Q64168",
                                        "answers": [
                                            {
                                                "answerPhrase": "Continuous",
                                                "answerId": "A61170",
                                            },
                                            {
                                                "answerPhrase": "Intermittent",
                                                "answerId": "A20225",
                                            },
                                            {
                                                "answerPhrase": "One time",
                                                "answerId": "A60315",
                                            },
                                            {
                                                "answerPhrase": "Unknown",
                                                "answerId": "A20040",
                                            },
                                        ],
                                    },
                                    {
                                        "optional": "false",
                                        "questionPhrase":
                                        "What kind of environment was the customer in?",
                                        "answerType": "DPD",
                                        "questionId": "Q100407",
                                        "answers": [
                                            {
                                                "answerPhrase": "Indoor",
                                                "answerId": "A101250",
                                            },
                                            {
                                                "answerPhrase": "Outdoor",
                                                "answerId": "A101251",
                                            },
                                            {
                                                "answerPhrase": "Other",
                                                "questions": [
                                                    {
                                                        "optional": "false",
                                                        "questionPhrase": "Please describe",
                                                        "answerType": "FFB",
                                                        "questionId": "Q64128",
                                                    },
                                                ],
                                                "answerId": "A68174",
                                            },
                                        ],
                                    },
                                ],
                                "answerId": "A20075",
                            },
                        ],
                    },
                ],
                "treeId": "TREE203927",
            },
        ],
    },
]


class RepairQuestionsSerializer(BaseGSXSerializer):
    data = serializers.JSONField()

    def create(self, validated_data):
        if is_in_dev_mode():
            return dummy_response
        req = GSXRequest(
            "repair",
            "questions",
            self.gsx_user_name,
            self.gsx_auth_token,
            self.gsx_ship_to,
        )
        data = copy.deepcopy(self.validated_data["data"])
        response = req.post(**data)
        return response
