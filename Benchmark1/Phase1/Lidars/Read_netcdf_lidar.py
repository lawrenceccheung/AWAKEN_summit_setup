#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:20:48 2024

@author: nbodini
"""
import xarray as xr

# Define the path to your NetCDF file
file_path = 'A1_profiling_lidar_10min.nc'

# Open the NetCDF file
ds = xr.open_dataset(file_path)

# Print the dataset information
print("Dataset information:")
print(ds)

# Print the variable names
print("\nVariable names:")
print(ds.variables)

# Print the dimensions
print("\nDimensions:")
print(ds.dims)

# Print coordinate values
print("\nCoordinates:")
for coord in ds.coords:
    print(f"{coord}: {ds.coords[coord].values}")

# Access specific variables
print("\nSample data from variable 'U':")
print(ds['U'])

