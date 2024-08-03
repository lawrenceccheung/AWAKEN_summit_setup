#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:14:37 2024

@author: nbodini
"""
import xarray as xr

# Open the NetCDF file
ds_temperature = xr.open_dataset('B_ASSIST_phase1.nc')

# Print information about the dataset
print("Information about the dataset:")
print(ds_temperature)

# Accessing data variables
print("\nData variables available:")
print(ds_temperature.data_vars)

# Accessing coordinates
print("\nCoordinates available:")
print(ds_temperature.coords)

# Accessing a specific variable
temperature_variable = ds_temperature['temperature']
print("\nTemperature data:")
print(temperature_variable)

# Accessing attributes
print("\nAttributes of temperature variable:")
print(temperature_variable.attrs)

# Closing the NetCDF file
ds_temperature.close()
