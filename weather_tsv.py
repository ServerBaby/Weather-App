"""

This script downloads the elastic search data to a tab separated values file

DRAFT VERSION - NOT WORKING PROPERLY YET

"""

import elasticsearch
import csv

es = elasticsearch.Elasticsearch(["127.0.0.1:9200"])

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

es_documents = res['hits']['hits']

print("Got %d hits" % res['hits']['total']['value'])

with open('weather.tsv', 'w') as csv_file:
	file_writer = csv.writer(csv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	file_writer.writerow(["id", "UTC time"]) 	# create header row
	for hit in es_documents:
		try:
			col1 = hit["_id"]
		except Exception:
			col1 = ""
		try:
			col2 = hit["properties"]["aifstime_utc"].decode('utf-8')
			col2 = col2.replace('\n', ' ')
		except Exception:
			col2 = ""
		try:
			col3 = hit["properties"]["apparent_t"].decode('utf-8')
			col3 = col3.replace('\n', ' ')
		except Exception:
			col3 = ""
		file_writer.writerow([col1, col2, col3])
