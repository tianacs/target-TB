#!/usr/bin/env python

"""
Trying to merge the JSON files.
16/12/2022
"""

import json
import copy

# load the skeleton
with open('skeleton.json', 'r+') as f:
    skeleton = json.load(f)
    # file is closed again after "with" block
    # TODO integrate with create_a_skeleton_JSON.py so file doesn't need to be written

# load the files to be merged
with open('TB_48.1.mykrobe.json', 'r') as f:
    JSON_One = json.load(f)

with open('TB_48.2.mykrobe.json', 'r') as f:
    JSON_Two = json.load(f)

# Start by working with the ["susceptibility"] level:

def filter_json (JSON, target):
    """
    Remove any variant calls not in the specificied target region
    """
    for drug, drug_prediction in JSON.items():
        if "called_by" in drug_prediction:
            for variant in dict(drug_prediction["called_by"]):
                if variant.split ("_")[0] != target:
                    del drug_prediction["called_by"][variant]
                if not(drug_prediction["called_by"]):
                    drug_prediction["predict"] = "S"
    return JSON

# Get only the "appropriate" resistance calls
# TODO rename these variables
kopie = copy.deepcopy (JSON_One["TB_48"]["susceptibility"])
filter_json (kopie, "gyrA")

kopie_two = copy.deepcopy (JSON_Two["TB_48"]["susceptibility"])
filter_json (kopie_two, "rpoB")

# For each drug listed under susceptibility
for drug in skeleton['TB_48']['susceptibility'].keys ():
    # Compare if the predicted status is the same in the two JSON files
    if kopie[drug]["predict"] == kopie_two[drug]['predict']:
        # If so copy the predicted status
        skeleton['TB_48']['susceptibility'][drug]['predict'] = copy.deepcopy (kopie[drug]['predict'])
        # ISSUE - what if both have a resistant call due to different genes?

    else:
        # If predict status is not the same, compare the statuses and copy according to the "R">"r">"S" priorities
        # ISSUE - when comparing the next two files - will those then overwrite the skeleton file?
        if kopie[drug]["predict"] == "R":
            skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (kopie[drug])
        elif kopie_two[drug]['predict'] == "R":
            skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (kopie_two[drug])
        elif kopie[drug]["predict"] == "r":
            skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (kopie[drug])
        elif kopie_two[drug]['predict'] == "r":
            skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (kopie_two[drug])

print (skeleton)
with open('test_out.json', 'w') as json_file:
    json.dump(skeleton, json_file, indent=4)