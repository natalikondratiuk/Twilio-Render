import json

from .router import Controller
from modules.worker import Worker

from objects.configs import Config

def parse_json(json_path: str) -> Config:
    with open(json_path) as fread:
        return Config(data_json=json.load(fread)).get_attributes

args = "external/config.json"
config = parse_json(args)
if isinstance(config, Config):
    worker = Worker(config=config)
    app = Controller(config.router_params).set_worker(worker).add_route.set_app
