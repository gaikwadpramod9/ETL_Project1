import json
import re
import os
import networkx as nx  # pip install networkx if missing
import pprint

#STEP 1: Data Extraction and Transformation

table_dict = {}
#Path of the directory or network drive where the JSON files are located
dir_path = r'D:\\Users\\Pramod_WS\\Workspace\\ETL_Project1-iteration1\\tables'

for path in os.listdir(dir_path):
    file = open(dir_path+'\\'+path)
    jsonData = json.load(file)
    #extract the from clause string from json file
    try:
        fromClauseString = jsonData['query']['L'][0]['M']['from']['S']
    except:
        try:
            fromClauseString = jsonData['query']['M']['from']['S']
        except:
            print('Datasource Schema unsupported for JSON file '+path)
    #extract first table name from 'from' string
    firstTableName = fromClauseString.partition(' ')[0]
    if firstTableName == '':
        firstTableName =fromClauseString.partition(' ')[2]
        firstTableName = firstTableName.partition(' ')[0]
    #extract rest of table names from 'from' string
    allTableNames = re.findall('join ([a-zA-Z._0-9-]+)',fromClauseString)
    if not allTableNames:
        allTableNames = re.findall('JOIN ([a-zA-Z._0-9-]+)',fromClauseString)
    if not allTableNames:
        allTableNames = []
    allTableNames.insert(0,firstTableName)
    #the filename is a table name (root relation for tables in 'from' clause)  
    filename = path[:-5]
    table_dict[filename] = allTableNames
    file.close()

#just for visualisation and printing the dictionary 
pp= pprint.PrettyPrinter()
pp.pprint(table_dict)


#STEP2: Data Visualization 