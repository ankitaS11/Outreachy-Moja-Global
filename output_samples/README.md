This folder contains the outputs generated from the script in `scripts/run.py` folder in this repository. To save your time, here are the images:

<img src="https://github.com/krshrimali/Outreachy-Internship/blob/f855c1127e490a37c039980759584698b99a322e/output_samples/climate.png" height=500 width=900></img>

<img src="https://github.com/krshrimali/Outreachy-Internship/blob/f855c1127e490a37c039980759584698b99a322e/output_samples/ecological_zone.png" height=500 width=900></img>

<img src="https://github.com/krshrimali/Outreachy-Internship/blob/f855c1127e490a37c039980759584698b99a322e/output_samples/soil_cover.png" height=500 width=900></img>

A sample `result.json` file which contains the label corresponding to each task (climate/soil cover/ecological zone) which has occured the most number of types for the given forest type in the concerned country. Here, the plots are for Australia.

```json
{
    "Chosen Forest Type": "Tropical dry forest",
    "CLIMATE": "Tropical rainforest climate",
    "SOIL": "Leptosol",
    "ECOLOGICAL_ZONE": "Tropical dry forest"
}
```

From the JSON file above, most of the areas in Australia having forest type as "Tropical Dry Forest" have:

1. Climate as "Tropical Rainforest Climate"
2. Soil as "Leptosol"
3. Ecological Zone as "Tropical Dry Forest"
