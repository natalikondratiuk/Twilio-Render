from __future__ import annotations

from typing import Annotated
from fastapi import FastAPI, APIRouter, Query

from modules.worker import Worker
from objects.configs import RouterParameters

from objects.schemas import Recipient
from objects.responses import SmsResponse

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
                                   response_model=SmsResponse)
        self._application.include_router(self._router)

        return self

    async def _send_sms(self, recipient: Annotated[Recipient, Query()]) -> SmsResponse:
        return await self._WORKER.send_sms(recipient)


