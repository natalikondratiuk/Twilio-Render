import os
from dotenv import load_dotenv
load_dotenv()

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

    async def send_sms(self, recipient: Recipient) -> SmsResponse:
        print(f"Phone: {recipient.phone}, type - {type(recipient.phone)}")
        message = self._client.messages.create(
            from_=self._twilio_params.phone,
            to=recipient.phone,
            body=recipient.message
        )
        date_created = message.date_created.strftime("%Y-%m-%d %H:%M:%S")

        return SmsResponse(
            host=message.from_,
            recipient=message.to,
            date_created=date_created,
            body=recipient.message
        )

    async def make_call(self, recipient: Recipient) -> CallResponse:
        response = VoiceResponse()
        response.say(recipient.message, language=self._twilio_params.language)

        call = await self._client.calls.create_async(
            to=recipient.phone,
            from_=self._twilio_params.phone,
            twiml=str(response)
        )

        return CallResponse(
            host=call.from_formatted,
            recipient=call.to_formatted,
            date_created=call.date_created,
            body=str(response)
        )