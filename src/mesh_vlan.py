import json
from dataclasses import dataclass
from typing import List

@dataclass
class SSID:
    name: str
    password: str

class MeshVLAN:
    def __init__(self):
        self.ssids = []
        self.radio_settings = {"2.4GHz": True, "5GHz": True}

    def create_ssid(self, name: str, password: str):
        ssid = SSID(name, password)
        self.ssids.append(ssid)
        return ssid

    def delete_ssid(self, name: str):
        self.ssids = [ssid for ssid in self.ssids if ssid.name != name]

    def update_radio_settings(self, settings: dict):
        self.radio_settings = settings

    def get_ssids(self):
        return self.ssids

    def get_radio_settings(self):
        return self.radio_settings

    def persist_settings(self):
        # Simulate persisting settings
        return self.radio_settings

    def get_dashboard(self):
        # Simulate getting dashboard data
        return {"ssids": [ssid.name for ssid in self.ssids], "radio_settings": self.radio_settings}
