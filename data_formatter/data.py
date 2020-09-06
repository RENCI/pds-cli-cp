import pandas as pd

def parseKey(s, delimiter="."):
        return s[:s.rindex(delimiter)], s[s.rindex(delimiter)+1:] #parse tx parallex ouput
    
def writeCSV(ret, outputFilePath,sep=","):
        df = []
        allData={}
        for uid, entry in enumerate(ret, start=1): # through list of maps                                                                                                                                                                                                                                                    
                print(uid)
                for mappedObject in entry['values']: #in form {'id':ID,'variableValue': {'value': VALUE}                                                                                                                                                                                                                    
                        attribute=mappedObject['id']
                        value=mappedObject['variableValue']['value']
                        if uid not in allData:
                                allData[uid]={}
                                allData[uid][attribute]=value
                        else:
                                allData[uid][attribute]=value
                                #del ret[k]                                                                                                                                                                                                                                                                                 
        for uid in allData:
                print("working on uid")
                print(uid)
                patientData=allData[uid]
                if bool(patientData['hasIntervention']):
                        finalRow=patientData['counts']
                        finalRow['AEs']=len(patientData['ae'])
                        finalRow['Intervents']=int(patientData['hasIntervention'])

                        finalRow['PDS:male']=0 if patientData['patient']['gender']=='female' else 1
                        finalRow['PDS:married']=1 if patientData['patient']['maritalStatus']=='M' else 0
                        finalRow['PDS:age']=int(patientData['patient']['age'])
                        address = patientData['patient'].get('address')
                        if address is None:
                                finalRow['PDS:lat']=None
                                finalRow['PDS:long']=None
                        else:
                                finalRow['PDS:lat'], finalRow['PDS:long']=address

                        df.append(finalRow)
                else:
                        print("did not write out patient data for "+str(uid)+" - No Intervention")

        df=pd.DataFrame(df)
        df.to_csv(outputFilePath, sep=sep, index=False)
        print("data written at "+ outputFilePath)
