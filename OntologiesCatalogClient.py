## This script generates segments for each pair of ontologies in the catalog based on three data requirements
from os import path
from os import walk
import requests

## 2)
def import_ontologies_into_catalog():
    ontologyCatalogURL = "http://localhost:8081/api/ontologies/import"
    basepath = "/Users/diegopessoa/Projects/phd/ontologies/conference/"
    ontologias = []
    for (dirpath, dirnames, filenames) in walk(basepath):
        ontologias.extend(list(filter(lambda x: not x.startswith('.') and x.endswith('.owl'), filenames)))
        break  # not recursive

    print(ontologias)

    for ontologia in ontologias:
        filename, file_extension = path.splitext(ontologia)
        data = "file://" + basepath + ontologia
        response = requests.post(ontologyCatalogURL, data=data)
        print(response)
        if response.status_code in (200,201):
            print("Ontologia",filename,"importada com sucesso no catálogo de ontologias!")

# import_ontologies_into_catalog()