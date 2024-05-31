#
#  Copyright (C) 2024 RapidSilicon
#  Authorized use only
#
from enum import Enum
from typing import Dict, Any
import copy

class RsMessageType(Enum):
    ERRO = "error"
    WARN = "warn"
    INFO = "info"

class RsMessage:
    def __init__(self, message_code, message_type, message_text):
        self.code = message_code
        self.type = message_type
        self.text = message_text

class RsMessageManager:
    messages = {
        101: RsMessage(101, RsMessageType.INFO, "This clock is disabled"),
        102: RsMessage(102, RsMessageType.INFO, "DSP is disabled"),
        103: RsMessage(103, RsMessageType.INFO, "Logic Element is disabled"),
        104: RsMessage(104, RsMessageType.INFO, "BRAM is disabled"),
        105: RsMessage(105, RsMessageType.INFO, "IO is disabled"),
        201: RsMessage(201, RsMessageType.WARN, "Clock is specified but no loads identified in other tabs"),
        202: RsMessage(202, RsMessageType.WARN, "Not enough {bank_type} banks powered at {voltage}V available"),
        301: RsMessage(301, RsMessageType.ERRO, "Invalid clock"),
        302: RsMessage(302, RsMessageType.ERRO, "Invalid clock on Port A"),
        303: RsMessage(303, RsMessageType.ERRO, "Invalid clock on Port B"),
        999: RsMessage(999, RsMessageType.ERRO, "Unknown error")
    }

    @staticmethod
    def get_message(message_code: int, params : Dict[str, Any] = None) -> RsMessage:
        message = RsMessageManager.messages.get(message_code)
        if message is not None:
            copied_message = copy.deepcopy(message)
            if params is not None:
                copied_message.text = copied_message.text.format(**params)
            return copied_message
        return RsMessageManager.messages[999]
