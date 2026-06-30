# -*- coding: utf-8 -*-

!pip install sunpy[all]

import os
from google.colab import drive

# 1. Mount your personal Google Drive
drive.mount('/content/drive')

# 2. Define a clean path inside your Drive to save your FITS files permanently
drive_data_dir = '/content/drive/MyDrive/SolarData'

import os
import numpy as np
import astropy.units as u
import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a

# 1. Define paths and expected final names
drive_data_dir = '/content/drive/MyDrive/SolarData'
expected_aia_name = "observation20_aia.fits"
expected_hmi_name = "observation20_hmi.fits"

local_aia_path = os.path.join(drive_data_dir, expected_aia_name)
local_hmi_path = os.path.join(drive_data_dir, expected_hmi_name)

time_range = a.Time('2020/11/11 18:00:00', '2020/11/11 18:00:10')
time_range_HMI = a.Time('2020/11/11 18:00:00', '2020/11/11 18:00:40')

# ----------------- 1. RETRIEVE OR DOWNLOAD AIA 193 Å -----------------
if os.path.exists(local_aia_path):
    print("🚀 AIA file found in Google Drive! Loading local file...")
    aia193 = sunpy.map.Map(local_aia_path)
else:
    print("📡 AIA file not found locally. Searching JSOC / VSO...")
    aia_query = Fido.search(time_range, a.Instrument.aia, a.Wavelength(193*u.angstrom))

    print("📥 Fetching AIA data from server...")
    # Providing the exact name structure inside the path argument forces the rename
    aia_download = Fido.fetch(aia_query, path=os.path.join(drive_data_dir, expected_aia_name))

    aia193 = sunpy.map.Map(local_aia_path)
    print(f"✅ Downloaded and saved AIA to: {local_aia_path}")

# ----------------- 2. RETRIEVE OR DOWNLOAD HMI MAGNETOGRAM -----------------
if os.path.exists(local_hmi_path):
    print("🚀 HMI file found in Google Drive! Loading local file...")
    hmi6163 = sunpy.map.Map(local_hmi_path)
else:
    print("📡 HMI file not found locally. Searching JSOC...")
    hmi_query = Fido.search(time_range_HMI, a.Instrument.hmi, a.Physobs.los_magnetic_field)

    print("📥 Fetching HMI data from server...")
    # Providing the exact name structure inside the path argument forces the rename
    hmi_download = Fido.fetch(hmi_query, path=os.path.join(drive_data_dir, expected_hmi_name))

    hmi6163 = sunpy.map.Map(local_hmi_path)
    print(f"✅ Downloaded and saved HMI to: {local_hmi_path}")

print("\n🎉 Maps successfully loaded!")
