import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from objects.configs import TwilioParameters
from objects.schemas import Recipient
from objects.responses import SmsResponse, CallResponse

class Twilio:
    def __init__(self, twilio_params: TwilioParameters):
        self._twilio_params: TwilioParameters = twilio_params

        self._client = Client(
            username=os.getenv("ACCOUNT_SID"),
            password=os.getenv("AUTH_TOKEN")
        )

    def _get_timestamp(self):
        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return timestamp

    async def send_sms(self, recipient: Recipient) -> SmsResponse:
        message = self._client.messages.create(
            from_=self._twilio_params.phone,
            to=recipient.phone,
            body=recipient.message
        )

        return SmsResponse(
            host=message.from_,
            recipient=message.to,
            date_created=self._get_timestamp(),
            body=recipient.message
        )

    async def make_call(self, recipient: Recipient) -> CallResponse:
        response = VoiceResponse()
        response.say(recipient.message, language=self._twilio_params.language)

        call = self._client.calls.create(
            to=recipient.phone,
            from_=self._twilio_params.phone,
            twiml=str(response)
        )

        return CallResponse(
            host=call.from_formatted,
            recipient=call.to_formatted,
            date_created=self._get_timestamp(),
            body=str(response)
        )