# Python program to demonstrate
# Conversion of JSON data to
# dictionary


# importing the module
import json

# Opening JSON file
with open('logement-encadrement-des-loyers.json') as json_file:
	data = json.load(json_file)

#print(data[3]['datasetid'])
#print(data[3]['recordid'])
#print(data[3]['fields'])
#print(data[3]['geometry'])
#print(data[3]['record_timestamp'])

print(len(data[3]))

print(data[3]['fields']['ref'])
print(data[3]['fields']['annee'])
print("Qartier {} : {}".format(data[3]['fields']['id_quartier'],data[3]['fields']['nom_quartier']))
