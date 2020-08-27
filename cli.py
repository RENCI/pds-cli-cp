import pprint
import sys
import yaml
import requests
import time
import argparse
import shutil

parser = argparse.ArgumentParser(description='pds cli for cp')
parser.add_argument('specName', help='spec name')
parser.add_argument('--libraryPath', nargs="*", default=[], help='python module path')
parser.add_argument('--nthreads', type=int, default=4, help='number of threads')
parser.add_argument('--level', type=int, default=0, help='level')
parser.add_argument('resourceTypesFile', help='resource types file')
parser.add_argument('patientIdsFile', help='patient id files')
parser.add_argument('timestamp', help='timestamp')
parser.add_argument('--pdsHost', default="localhost", help='pds host')
parser.add_argument('--pdsPort', type=int, default=8080, help='pds port')
parser.add_argument('--configDir', help='config dir')

args = parser.parse_args()

specName = args.specName
libraryPath = args.libraryPath
nthreads = args.nthreads
level = args.level
resourceTypesFile = args.resourceTypesFile
patientIdsFile = args.patientIdsFile
timestamp = args.timestamp
pdsPort = args.pdsPort
pdsHost = args.pdsHost
configDir = args.configDir

if configDir is not None:
    shutil.copy(f"config/{specName}", configDir)
    for p in libraryPath:
        shutil.copytree(f"config/{p}", f"{configDir}/{p}", dirs_exist_ok=True)

with open(patientIdsFile) as f:
    patientIds = yaml.safe_load(f)

with open(resourceTypesFile) as f:
    resourceTypes = yaml.safe_load(f)

json_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
fhirStart = time.time()
resp = requests.post(f"http://localhost:{pdsPort}/v1/plugin/pdspi-fhir-example/resource", json={
    "resourceTypes": resourceTypes,
    "patientIds": patientIds
}, headers=json_headers)

fhirEnd = time.time()

print(fhirEnd - fhirStart)

if resp.status_code != 200:
    print(resp.text)

fhir = resp.json()

mapperStart = time.time()
print(f"libraryPath = {libraryPath}")
resp = requests.post(f"http://localhost:{pdsPort}/v1/plugin/pdspi-mapper-parallex-example/mapping", json={
    "data": fhir,
    "settingsRequested": {
        "modelParameters": [{
            "id": "specName",
            "parameterValue": {"value": specName}
        }, {
            "id": "nthreads",
            "parameterValue": {"value": nthreads}
        }, {
            "id": "level",
            "parameterValue": {"value": level}
        }, {
            "id": "libraryPath",
            "parameterValue": {"value": libraryPath}
        }]
    },
    "patientVariables": [],
    "patientIds": patientIds,
    "timestamp": timestamp
}, headers=json_headers)

mapperEnd = time.time()

print(mapperEnd - mapperStart)

if resp.status_code == 200:
    ret = resp.json()

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(ret)
else:
    print(resp.text)


