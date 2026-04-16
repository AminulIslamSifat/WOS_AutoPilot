import json

path = "cache/chief_profile.json"

with open(path, "r") as file:
    data = json.load(file)


rois = []
for res in data:
    rois.append(res["box"])

print(rois)