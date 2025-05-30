from dataclasses import dataclass

@dataclass
class TwilioParameters:
    phone: str
    language: str