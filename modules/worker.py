from __future__ import annotations

from objects.configs import Config
from tools.twilio import Twilio

from objects.schemas import Recipient
from objects.responses import SmsResponse, CallResponse

class Worker:
    def __init__(self, config: Config):
        self._twilio = Twilio(
            twilio_params=config.twilio_params
        )

    async def run(self) -> Worker:
        return self

    async def send_sms(self, recipient: Recipient) -> SmsResponse:
        return await self._twilio.send_sms(recipient)

    async def make_call(self, recipient: Recipient) -> CallResponse:
        return await self._twilio.make_call(recipient=recipient)
