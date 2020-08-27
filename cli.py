import pprint
import sys
import yaml
import requests
import time
import argparse
import shutil
import os
from data_formatter.data import writeCSV
from tempfile import mkstemp
import json

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
parser.add_argument('--tmpDir', default="/tmp", help='tmp dir')
parser.add_argument('outputCSV', help='output CSV')
parser.add_argument('--outputJSON', help='output JSON')

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
outputCSV = args.outputCSV
outputJSON = args.outputJSON
tmpDir = args.tmpDir

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
    "patientIds": patientIds,
    "outputFile": "data"
}, stream=True)

fhirEnd = time.time()

print(fhirEnd - fhirStart)

if resp.status_code != 200:
    print(resp.text)

fhir = {
    "data": resp.json(),
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
        }, {
            "id": "outputPath",
            "parameterValue": {"value": outputJSON}
        }]
    },
    "patientVariables": [],
    "patientIds": patientIds,
    "timestamp": timestamp
}
# print("receiving file...")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
# fileBegin = time.time()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
# fd, tmpfile = mkstemp(dir=tmpDir)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
# os.close(fd)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

# try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
#     with open(tmpfile, "wb") as tmp:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
#         tmp.write('{"data":'.encode())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
#         for content in resp.iter_content(1024*1024):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
#             tmp.write(content)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
#         tmp.write((',"settingsRequested":' + json.dumps({                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
#             "modelParameters": [{                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
#                 "id": "specName",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
#                 "parameterValue": {"value": specName}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
#             }, {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#                 "id": "nthreads",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
#                 "parameterValue": {"value": nthreads}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
#             }, {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#                 "id": "level",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
#                 "parameterValue": {"value": level}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
#             }, {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#                 "id": "libraryPath",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
#                 "parameterValue": {"value": libraryPath}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
#             }]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
#         }) + ',"patientVariables":' + json.dumps([]) + ',"patientIds":' + json.dumps(patientIds) + ',"timestamp":' + json.dumps(timestamp) + '}').encode())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
#     fileEnd = time.time()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
#     print(fileEnd - fileBegin)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
#     print("send request to mapper")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
mapperStart = time.time()
outputJSON_path = os.path.join(tmpDir, outputJSON)
with open(outputJSON_path, "w") as fp:
    pass
#     with open(tmpfile, "rb") as fhir:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
resp = requests.post(f"http://localhost:{pdsPort}/v1/plugin/pdspi-mapper-parallex-example/mapping", json=fhir, headers=json_headers)

# finally:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
#     os.remove(tmpfile)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

mapperEnd = time.time()

print(mapperEnd - mapperStart)

print(resp.status_code)
if resp.status_code == 200:
    ret = resp.json()
elif resp.status_code == 204:
    with open(outputJSON_path) as o:
        ret = json.load(o)
else:
    print(resp.text)

if ret is not None:
    writeCSV(ret, outputCSV)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(ret)
