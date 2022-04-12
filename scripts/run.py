"""
Author: Ankita Sharma (https://www.github.com/ankitaS11)

## What does this script do?

1. Automates the process of finding "the most common" climate/soil/ecological zone type
for the given forest type. The "most common" type would be the label that occupies
"majority" of the region for the given forest type.
2. Saves the visualizations in the respective files, namely: "climate.png", "soil_cover.png"
and "ecological_zone.png".
3. Saves the output to a JSON File (result.json).
"""

import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import numpy as np
from collections import Counter

import os
import subprocess
import json

import Datasets
# Unused for now, but we can use later
# from cfg import countries_dict

# Example: For INDIA
# json_paths = {
#     "COUNTRY": "https://datasets.mojaglobal.workers.dev/0:/Administrative/Boundaries/Level2%20by%20Country/IND/IND_AL2_India.json",
#     "COUNTRY_GEZ": "https://datasets.mojaglobal.workers.dev/0:/Administrative/Boundaries/Level2%20by%20Country/IND/IND_AL2_India_GEZ.json",
#     "CLIMATE": "https://datasets.mojaglobal.workers.dev/0:/Climate/IPCC_ClimateZoneMap_Vector.geojson",
#     "SOIL": "https://datasets.mojaglobal.workers.dev/0:/Soil/World%20Soil%20Resources/World_Soil_Resources_wgs84.geojson",
#     "ECOLOGICAL_ZONE": "https://datasets.mojaglobal.workers.dev/0:/Bioclimatic&EcologicalZones/Global_Ecological_Zone_GEZ/GlobalEcologicalZone_GEZFAO2010.json"
# }

# Only COUNTRY and COUNTRY_GEZ urls need to be changed
# Example: For AUSTRALIA
json_paths = {
    "COUNTRY": "https://datasets.mojaglobal.workers.dev/0:/Administrative/Boundaries/Level2%20by%20Country/AUS/AUS_AL2_Australia.json",
    "COUNTRY_GEZ": "https://datasets.mojaglobal.workers.dev/0:/Administrative/Boundaries/Level2%20by%20Country/AUS/AUS_AL2_Australia_GEZ.json",
    "CLIMATE": "https://datasets.mojaglobal.workers.dev/0:/Climate/IPCC_ClimateZoneMap_Vector.geojson",
    "SOIL": "https://datasets.mojaglobal.workers.dev/0:/Soil/World%20Soil%20Resources/World_Soil_Resources_wgs84.geojson",
    "ECOLOGICAL_ZONE": "https://datasets.mojaglobal.workers.dev/0:/Bioclimatic&EcologicalZones/Global_Ecological_Zone_GEZ/GlobalEcologicalZone_GEZFAO2010.json"
}

for json_path in json_paths.values():
    if not os.path.exists(json_path.split("/")[-1]):
        subprocess.run(["wget", json_path])

datasets = {}
df_reference = None
forest_type = "Tropical dry forest"
result = {
    "Chosen Forest Type": forest_type
}
for key, admin_path in json_paths.items():
    path = admin_path.split("/")[-1]
    assert os.path.isfile(path), f"Given path {path} is not a file"

    if "COUNTRY" in key:
        ds = Datasets.Dataset(path)
        df = ds.load_dataset()
        if "COUNTRY_GEZ" in key:
            df_reference = df[df['gez_name'] == forest_type]
        datasets[key] = [ds, df]
        continue
    elif "CLIMATE" in key:
        ds = Datasets.ClimateClass(path)
        label = "CLASS_NAME"
    elif "SOIL" in key:
        ds = Datasets.SoilClass(path)
        label = "IPCC"
    elif "ECOLOGICAL_ZONE" in key:
        ds = Datasets.EcologicalClass(path) 
        label = "gez_name"
    else:
        continue

    df = ds.load_dataset()
    assert df_reference is not None, "Reference dataframe is not loaded yet"
    datasets[key] = [ds, ds.process_dataset(df_reference=df_reference)]
    ds.plot(df_reference=df_reference, show=False, save_output=True)

    c = Counter([x for x in datasets[key][1][label]])
    # Get the label/category which occupies "most of the region" for the given forest type
    most_common_key = c.most_common()[0][0]
    result[key] = most_common_key

with open('result.json', 'w') as out_file:
    json.dump(result, out_file, indent=4)

print("Output file has been written to result.json in your current folder. Thank you!")