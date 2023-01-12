#!/usr/bin/env pythonjson_dict

"""
Trying to merge the JSON files.
12/01/2022
"""

import json
import copy

# TODO merge the levels other than "susceptibility"?
# TODO double check the output so far

def filter_json (json_dict, target):
    """
    Remove any variant calls not in the specificied target region
    """
    for drug, drug_prediction in json_dict.items():
        if "called_by" in drug_prediction:
            for variant in dict(drug_prediction["called_by"]):
                if variant.split ("_")[0] != target:
                    del drug_prediction["called_by"][variant]
                if not(drug_prediction["called_by"]):
                    drug_prediction["predict"] = "S"
    return json_dict

def merge_susceptibility (json_dict):
    """
    Merge the susceptibility calls of an individual mykrobe JSONs into the skeleton
    """
    for drug in skeleton['TB_48']['susceptibility'].keys ():
        # If there is an drug variant entry in the skeleton,
        # Check if the resistant call is the same.
        # If not, compare acc. to priorities and overwrite if appropriate
        if skeleton['TB_48']['susceptibility'][drug]:
            if skeleton['TB_48']['susceptibility'][drug]['predict'] == json_dict[drug]["predict"]:
                pass
            else:
                if json_dict[drug]["predict"] == "R":
                    skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (json_dict[drug])
                elif json_dict[drug]["predict"] == "r":
                    skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (json_dict[drug])
        else:
            skeleton['TB_48']['susceptibility'][drug] = copy.deepcopy (json_dict[drug])

########################################################################
# Make a skeleton
########################################################################

# Load the JSON file into a dictionary
with open('TB_48.1.mykrobe.json', 'r') as f:
    data = json.load(f)

# Initialize an empty dictionary to hold the skeleton
skeleton = {}

# Set the depth of the skeleton you want to copy
max_depth = 2

# Traverse the dictionary and copy the keys up to the specified depth
def copy_skeleton(data, skeleton, depth=0):
    if depth > max_depth:
        return
    for key, value in data.items():
        if isinstance(value, dict):
            skeleton[key] = {}
            copy_skeleton(value, skeleton[key], depth+1)
        else:
            skeleton[key] = None

copy_skeleton(data, skeleton)

########################################################################

targets = [ "gyrA", "rpoB", "rv0678", "rpsL", "rplC", "rrs", "rrl",
            "fabG1", "inhA", "tlyA", "katG", "pncA", "eis", "embB", "ethA", "gidB"]

for count, drug_target in enumerate (targets):
    with open(f'TB_48.{count+1}.mykrobe.json', 'r') as f:
        target_json = json.load(f)

    filtered_JSON = copy.deepcopy (target_json["TB_48"]["susceptibility"])
    filter_json (filtered_JSON, drug_target)

    if filtered_JSON:
        merge_susceptibility (filtered_JSON)

with open(f'merged.output.json', 'w') as json_file:
    json.dump(skeleton, json_file, indent=4)
