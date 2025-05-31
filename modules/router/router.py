from __future__ import annotations

from typing import Annotated, Union
from fastapi import FastAPI, APIRouter, Query, Response, status

from modules.worker import Worker
from objects.configs import RouterParameters

from objects.schemas import Recipient
from objects.responses import SmsResponse, CallResponse, FailedResponse

class Controller:
    _WORKER: Worker

    def __init__(self, config: RouterParameters):
        self._config = config

        self._router: APIRouter = APIRouter()
        self._application: FastAPI = FastAPI()

    @property
    def set_app(self):
        return self._application

    def set_worker(self, worker: Worker) -> Controller:
        self._WORKER = worker
        return self

    @property
    def add_route(self) -> Controller:
        self._router.add_api_route(self._config.sms_params.route, self._send_sms, methods=[self._config.sms_params.methods],
                                   response_model=Union[SmsResponse, FailedResponse])
        self._router.add_api_route(self._config.voice_params.route, self._make_call,
                                   methods=[self._config.voice_params.methods],
                                   response_model=Union[CallResponse, FailedResponse])

        self._application.include_router(self._router)

        return self

    async def _send_sms(self, recipient: Annotated[Recipient, Query()], response: Response):
        '''try:
            return await self._WORKER.send_sms(recipient)
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return FailedResponse()'''
        return await self._WORKER.send_sms(recipient)

    async def _make_call(self, recipient: Annotated[Recipient, Query()], response: Response):
        try:
            return await self._WORKER.make_call(recipient)
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return FailedResponse()

