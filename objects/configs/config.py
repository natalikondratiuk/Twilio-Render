from __future__ import annotations

import logging
from typing import Union
from aenum import Enum
from dataclasses import dataclass

from objects.configs import RouterParameters, TwilioParameters

class ConfigKeys(Enum):
    router_params: RouterParameters = RouterParameters
    twilio_params: TwilioParameters = TwilioParameters

@dataclass
class Config:
    def __init__(self, data_json: dict, debug: bool = False):
        self._logger: logging.Logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(logging.DEBUG if debug else logging.INFO)

        self._data_json: dict = data_json

        self.router_params: Union[RouterParameters, ellipsis] = ...
        self.twilio_params: Union[TwilioParameters, ellipsis] = ...

    @property
    def get_attributes(self) -> Union[Config, None]:
        try:
            for attribute, value in self._data_json.items():
                self.__setattr__(
                    ConfigKeys.__getitem__(attribute).name,
                    ConfigKeys.__getitem__(attribute).value(**value)
                )
            return self
        except TypeError:
            self._logger.error("Wrong JSON format, unexpected keyword argument in config")
            return
        except KeyError:
            self._logger.error("Wrong JSON key name, please, review Config and ConfigKeys "
                               "fields and name them as config.json keys")