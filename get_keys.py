from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH

import requests

# Define Variables
PSSH_VALUE = ".....=="
LICENSE_URL = "https://...."
WVD_DEVICE_FILE = "Your WVD dump from you own Android Device"

# prepare pssh
pssh = PSSH(PSSH_VALUE)

# load device
device = Device.load(WVD_DEVICE_FILE)

# load cdm
cdm = Cdm.from_device(device)

# open cdm session
session_id = cdm.open()

# get license challenge
challenge = cdm.get_license_challenge(session_id, pssh)

# send license challenge (assuming a generic license server SDK with no API front)
licence = requests.post(LICENSE_URL, data=challenge)
licence.raise_for_status()

# parse license challenge
cdm.parse_license(session_id, licence.content)

# print keys
for key in cdm.get_keys(session_id):
    print(f"[{key.type}] {key.kid.hex}:{key.key.hex()}")
    
# Write CONTENT keys to file
with open('keys.txt', 'w') as file:
    for key in cdm.get_keys(session_id):
        if key.type == "CONTENT":
            file.write(f"{key.kid.hex}:{key.key.hex()}\n")

# close session, disposes of session data
cdm.close(session_id)

print("Keys have also been saved to keys.txt")
