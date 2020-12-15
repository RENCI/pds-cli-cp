import pandas as pd
import csv

def parseKey(s, delimiter="."):
        return s[:s.rindex(delimiter)], s[s.rindex(delimiter)+1:] #parse tx parallex ouput
    
def writeCSV(ret, outputFilePath,sep="|"):
        df = []
        allData=[]
        columnnames = []

        for uid, entry in enumerate(ret, start=1): # through list of maps                                                                                                                                                                                                                                                    
                # print(uid)
                row = {}
                for mappedObject in entry['values']: #in form {'id':ID,'variableValue': {'value': VALUE}                                                                                                                                    

                        attribute=mappedObject['id']
                        value=mappedObject['variableValue']['value']

                        row[attribute]=value
                        if attribute not in columnnames:
                                columnnames.append(attribute)
                allData.append(row)
                #del ret[k]                                                                                                                                                                             
        dataarray=list(map(lambda row: list(map(lambda columnname: row.get(columnname), columnnames)), allData))

        df=pd.DataFrame(dataarray, columns=columnnames)
        df.sort_values(columnnames[0], inplace=True)
        df.to_csv(outputFilePath, sep=sep, quoting=csv.QUOTE_ALL, index=False)
        print("data written at "+ outputFilePath)
