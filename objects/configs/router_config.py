from dataclasses import dataclass

@dataclass
class SmsParameters:
    route: str
    methods: str

@dataclass
class VoiceParameters:
    route: str
    methods: str

@dataclass
class RouterParameters:
    sms_params: SmsParameters
    voice_params: VoiceParameters

    def __post_init__(self):
        self.sms_params = SmsParameters(**self.sms_params)
        self.voice_params = VoiceParameters(**self.voice_params)