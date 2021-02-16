#!/usr/bin/env python3

"""Download/Save the contents the user's ElasticSearch Index

This script allows the user to download and save the contents of the user's
elasticSearch index to a text file.  Can be used as a back up if data is lost
or deleted.

This script requires two modules from Pypi be installed within the Python 
environment you are running this script in. The two modules are elasticsearch 
and json.  elasticsearch module is used to access the data from an 
Elasticsearch index, and json module is used to transform the data into the
correct format.

This script currently contains two options:
1. Option 1 downloads the content of the Elasticsearch documents as a list
2. Option 2 downloads the content of the Elasticsearch documents as the text
    of a command to re-add the documents to an index as needed.

"""
import elasticsearch
import json

"""
Connects to the ElasticSearch server
Can replace IP and Port if if different
"""
es = elasticsearch.Elasticsearch(["127.0.0.1:9200"])

"""
Accesses the required index and searches for the required data
Can change:
    index= relevant index name
    query= to whatever query brings up the elastic search documents wanted to be downloaded/saved
    size= if not included defaults to 10, can be changed to a maximum of 10,000
          Currently set to download the first 100 results where "wmo" = "99435"
"""
res = es.search(index="weather_index", body={
					"query": {
						"bool": {
							"must": [
								{"match": {"wmo": "99435"}}
							]
						}
					}
				},
				size=100)

"""Accesses just the relevant part of the above query """
es_documents = res['hits']['hits']

"""
Can change name of the txt file data is saved to
"""
filename = "weather_save_4.txt"

"""
Prints the number of elastic search documents ["hits"] to the console.
Not the same number of documents that will be downloaded if the number of documents 
is greater than the number of documents specified in the query above.
"""
print("Got %d hits" % res['hits']['total']['value'])
print("Saving to file: " + filename)

"""
Saves elastic search documents to file:
First option saves the documents as a list,
Second option saves the documents as the text of a command that can be copied and pasted into 
Kibana Dev Tools to re-add the documents back into the index
"""
with open(filename, 'a') as f:
	# 'a' appends it to txt doc if it already exists rather than overwriting it
	# Can replace 'a' with 'w' if you wish to overwrite existing data
	""" Option 1 """
	# 	f.write(str(es_documents))
	""" Option 2 """
	try:
		for hit in es_documents:
			f.write("POST /weather_index/_doc/" + str(hit["_id"]) + '\n' + str(json.dumps(hit["_source"])) + '\n\n')
	except Exception:
		f.write("Error while downloading")
