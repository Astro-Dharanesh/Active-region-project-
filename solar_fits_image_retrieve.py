!pip install sunpy[all]

import os
from google.colab import drive

# 1. Mount your personal Google Drive
drive.mount('/content/drive')

# 2. Define a clean path inside your Drive to save your FITS files permanently
drive_data_dir = '/content/drive/MyDrive/SolarData'

import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
import sunpy.map
from sunpy.net import Fido
from sunpy.net import attrs as a
import pandas as pd


local_aia_path = "/content/drive/MyDrive/SolarData/observation20_aia.fits/aia.lev1.193A_2020_11_11T18_00_04.84Z.image_lev1.fits"
local_hmi_path = "/content/drive/MyDrive/SolarData/observation20_aia.fits/observation20_hmi.fits/hmi.m_45s.2020.11.11_18_01_30_TAI.magnetogram.fits"

# ----------------- 1. RETRIEVE OR DOWNLOAD AIA 193 Å -----------------
if os.path.exists(local_aia_path):
    print("🚀 AIA file found in Google Drive! Loading local file...")
    aia193 = sunpy.map.Map(local_aia_path)
else:
    print("📡 AIA file not found locally. Searching JSOC / VSO...")

# ----------------- 2. RETRIEVE OR DOWNLOAD HMI MAGNETOGRAM -----------------
if os.path.exists(local_hmi_path):
    print("🚀 HMI file found in Google Drive! Loading local file...")
    hmi6163 = sunpy.map.Map(local_hmi_path)
else:
    print("📡 HMI file not found locally. Searching JSOC...")

print("\n🎉 Maps successfully loaded! Metadata Verification:")
print(f"AIA Observation: {aia193.date}, Wavelength: {aia193.wavelength}")
print(f"HMI Observation: {hmi6163.date}, Measurement: {hmi6163.measurement}")

AIA_files = local_aia_path
AIA_files
aia193 = sunpy.map.Map(AIA_files)
aia193.meta
plt.figure(figsize=(8, 8))
aia193.plot(clip_interval=(1, 99.99) * u.percent)

HMI_files = local_hmi_path
HMI_files
hmi6163 = sunpy.map.Map(HMI_files)
hmi6163.meta
plt.figure(figsize=(8, 8))
im = hmi6163.plot(cmap="hmimag")  # store the mappable
plt.colorbar(im)

aia_reprojected = aia193.reproject_to(hmi6163.wcs)
aia_reprojected.nickname = 'AIA 193 Å (Reprojected)' #hmi ma 0.5 ra aia 0.6, reallign garna namilne bhayako le aia hmi equivalent grana lageko
from matplotlib.colors import Normalize
# Create the figure
fig = plt.figure(figsize=(12, 5))

# AIA 193 Å Plot
ax1 = fig.add_subplot(121, projection=aia_reprojected)
im1 = aia_reprojected.plot(axes=ax1, clip_interval=(1, 99.9) * u.percent)
ax1.set_title("AIA 193 Å 2024/03/24", fontsize=14)
cb1 = fig.colorbar(im1, ax=ax1, orientation='vertical', fraction=0.046, pad=0.04)
cb1.set_label("Intensity DN")
ax1.invert_xaxis()
ax1.invert_yaxis()

# HMI 6173 Å Plot
ax2 = fig.add_subplot(122, projection=hmi6163)
im2 = hmi6163.plot(axes=ax2, cmap="hmimag", norm=Normalize(-500, 500))
ax2.set_title("HMI 6173 Å  2024/03/24", fontsize=14)
cb2 = fig.colorbar(im2, ax=ax2, orientation='vertical', fraction=0.046, pad=0.04)
cb2.set_label("B$_{LOS}$ [G]")
ax2.invert_xaxis()
ax2.invert_yaxis()

plt.tight_layout(pad=1.0)
# plt.savefig("/Users/khagendrakatwal/Desktop/Paper_one/Code/Plots/AIA_HMI_Aligned_map.pdf", dpi=600, bbox_inches='tight')
plt.show()

from astropy.coordinates import SkyCoord

# Define corners in the AIA coordinate frame (matches HMI via reprojection)
aia_bottom_left = SkyCoord(385 * u.arcsec, -340 * u.arcsec, frame=aia_reprojected.coordinate_frame)
aia_top_right = SkyCoord(585 * u.arcsec, -500 * u.arcsec, frame=aia_reprojected.coordinate_frame)

# Create figure
fig = plt.figure(figsize=(16, 6), dpi=900)

#AIA Plot (reprojected to HMI frame)
ax1 = fig.add_subplot(121, projection=aia_reprojected)
im1 = aia_reprojected.plot(axes=ax1, clip_interval=(1, 99.9) * u.percent)

# Draw selected quadrangle
aia_reprojected.draw_quadrangle(
    bottom_left=aia_bottom_left,
    top_right=aia_top_right,
    axes=ax1,
    edgecolor='black',
    linestyle='--',
    linewidth=2
)

# AIA Labels & Settings
ax1.set_title("AIA 193 Å 2025/04/16", fontsize=16)
ax1.set_xlabel("Helioprojective Longitude [arcsec]", fontsize=16)
ax1.set_ylabel("Helioprojective Latitude [arcsec]", fontsize=16)
ax1.tick_params(labelsize=16)
ax1.invert_xaxis()
ax1.invert_yaxis()

# AIA Colorbar
cbar1 = plt.colorbar(im1, ax=ax1, orientation='vertical', pad=0.03)
cbar1.set_label('Intensity [DN]', fontsize=14)
cbar1.ax.tick_params(labelsize=14)

#HMI Plot (original)
ax2 = fig.add_subplot(122, projection=hmi6163)
im2 = hmi6163.plot(axes=ax2, cmap="hmimag", norm=Normalize(-500, 500))

# Draw the same quadrangle
hmi6163.draw_quadrangle(
    bottom_left=aia_bottom_left,
    top_right=aia_top_right,
    axes=ax2,
    edgecolor='black',
    linestyle='--',
    linewidth=2
)

# HMI Labels & Settings
ax2.set_title("HMI 6173 Å  2025/04/16 00:00:00", fontsize=16)
ax2.set_xlabel("Helioprojective Longitude [arcsec]", fontsize=16)
ax2.set_ylabel("Helioprojective Latitude [arcsec]", fontsize=16)
ax2.tick_params(labelsize=14)
ax2.invert_xaxis()
ax2.invert_yaxis()

# HMI Colorbar
cbar2 = plt.colorbar(im2, ax=ax2, orientation='vertical', pad=0.03)
cbar2.set_label('B$_{LOS}$ [G]', fontsize=16)
cbar2.ax.tick_params(labelsize=16)
# Add annotations
ax1.text(0.02, 0.95, 'a', transform=ax1.transAxes, fontsize=25, fontweight='bold', va='top')
ax2.text(0.02, 0.95, 'b', transform=ax2.transAxes, fontsize=25, fontweight='bold', va='top')

plt.show()

import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import SkyCoord
import sunpy.map
from matplotlib.colors import Normalize

# Assuming aia193 and hmi6163 are already defined from previous successful executions

# Re-define aia_reprojected, aia_bottom_left, aia_top_right, and aia_submap
aia_reprojected = aia193.reproject_to(hmi6163.wcs)
aia_reprojected.nickname = 'AIA 193 Å (Reprojected)'

aia_bottom_left = SkyCoord(385 * u.arcsec, -340 * u.arcsec, frame=aia_reprojected.coordinate_frame)
aia_top_right = SkyCoord(585 * u.arcsec, -500 * u.arcsec, frame=aia_reprojected.coordinate_frame)

aia_submap = aia_reprojected.submap(bottom_left=aia_bottom_left, top_right=aia_top_right)
hmi_submap = hmi6163.submap(bottom_left=aia_bottom_left, top_right=aia_top_right)

# Create the figure with two subplots for the active region
fig = plt.figure(figsize=(12, 6))

# AIA Active Region Plot
ax1 = fig.add_subplot(121, projection=aia_submap)
im1 = aia_submap.plot(axes=ax1, clip_interval=(1, 99.9) * u.percent)
ax1.set_title("AIA 193 Å Active Region", fontsize=14)
ax1.set_xlabel("Helioprojective Longitude [arcsec]", fontsize=12)
ax1.set_ylabel("Helioprojective Latitude [arcsec]", fontsize=12)
ax1.tick_params(labelsize=10)
cb1 = fig.colorbar(im1, ax=ax1, orientation='vertical', fraction=0.046, pad=0.04)
cb1.set_label("Intensity [DN]", fontsize=12)
ax1.invert_xaxis()
ax1.invert_yaxis()

# HMI Active Region Plot
ax2 = fig.add_subplot(122, projection=hmi_submap)
im2 = hmi_submap.plot(axes=ax2, cmap="hmimag", norm=Normalize(-500, 500))
ax2.set_title("HMI 6173 Å Active Region", fontsize=14)
ax2.set_xlabel("Helioprojective Longitude [arcsec]", fontsize=12)
ax2.set_ylabel("Helioprojective Latitude [arcsec]", fontsize=12)
ax2.tick_params(labelsize=10)
cb2 = fig.colorbar(im2, ax=ax2, orientation='vertical', fraction=0.046, pad=0.04)
cb2.set_label("B$_{LOS}$ [G]", fontsize=12)
ax2.invert_xaxis()
ax2.invert_yaxis()

plt.tight_layout(pad=1.0)
plt.show()

from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np

# Convert corners to pixel coordinates (floats)
aia_pix_bl = aia_reprojected.world_to_pixel(aia_bottom_left)
aia_pix_tr = aia_reprojected.world_to_pixel(aia_top_right)

# Create submaps from the defined region
aia_submap = aia_reprojected.submap(bottom_left=aia_bottom_left, top_right=aia_top_right)
hmi_submap = hmi6163.submap(bottom_left=aia_bottom_left, top_right=aia_top_right)

# --- AIA statistics ---
aia_data = aia_submap.data
aia_flux = np.sum(aia_data)
aia_mean_intensity = np.mean(aia_data)
aia_std_noise = np.std(aia_data, ddof=1)  # empirical noise (standard deviation)
aia_sem = aia_std_noise / np.sqrt(aia_data.size)  # standard error of the mean

# --- HMI statistics ---
hmi_data = hmi_submap.data
hmi_flux = np.sum(hmi_data)
hmi_mean_intensity = np.mean(hmi_data)
hmi_std_noise = np.std(hmi_data, ddof=1)
hmi_sem = hmi_std_noise / np.sqrt(hmi_data.size)

# --- Print results ---
print(f"Mean AIA intensity: {aia_mean_intensity:.3f}")
print(f"Total AIA flux: {aia_flux:.3f}")
print(f"AIA noise (std): {aia_std_noise:.3f}")
print(f"AIA standard error of mean: {aia_sem:.3f}")

print(f"Mean HMI intensity: {hmi_mean_intensity:.3f}")
print(f"Total HMI flux: {hmi_flux:.3f}")
print(f"HMI noise (std): {hmi_std_noise:.3f}")
print(f"HMI standard error of mean: {hmi_sem:.3f}")
hmi_abs_data = np.abs(hmi_data)

print("Absolute HMI Intensity Statistics:")
print(f"  Max: {np.max(hmi_abs_data):.2f}")
print(f"  Min: {np.min(hmi_abs_data):.2f}")
print(f"  Mean: {np.mean(hmi_abs_data):.2f}")
print(f"  Std Dev: {np.std(hmi_abs_data):.2f}")

print("\nNet HMI Intensity Statistics (signed data):")
print(f"  Mean: {np.mean(hmi_data):.2f}")
print(f"  Total Flux: {np.sum(hmi_data):.2f}")
