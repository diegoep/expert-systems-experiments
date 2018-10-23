import requests
import json
import logging

## 1) Gerar alinhamentos das ontologias/segmentos importados no catálogo para cada matcher.
## 2) Comparar conjunto de treinamento

# Carregar ontologias
def executeAlignments():
    logging.getLogger().setLevel(logging.INFO)
    matchersCatalogURL = "http://localhost:8888/api/ontologies"
    response = requests.get(matchersCatalogURL)
    ontologies = json.loads(response.text)
    ## Executar alinhamento para cada par de ontologia
    ## Fazer combinações...
    exps = ['exp2', 'exp3', 'exp4']
    logging.info("Executando alinhamentos de ontologias")
    for exp in exps:
        logging.info("******************** Alinhando ontologias do experimento {} *********************".format(exp))
        ontologiesToAlign = list(filter(lambda o: o['experiment'] == exp, ontologies))

        alignmentDict = {}

        for idx, ontologyToAlign in enumerate(ontologiesToAlign):
            source = str(ontologyToAlign['description']).split("-")[2]
            target = str(ontologyToAlign['description']).split("-")[3].split(".owl")[0]
            if not source + '-' + target in alignmentDict:
                alignmentDict[source + '-' + target] = {}
            if idx % 2 == 0:
                alignmentDict[source+'-'+target]['source'] = ontologyToAlign['file']
            else:
                alignmentDict[source+'-'+target]['target'] = ontologyToAlign['file']

        ## Varrer cada elemento do dicionario e executar os indices source vs target em cada matcher
        for dic in alignmentDict:
            sourceOntology = alignmentDict[dic]['source']
            targetOntology = alignmentDict[dic]['target']
            matchersEndpoint = "http://localhost:8888/api/matcher"
            response = requests.get(matchersEndpoint)
            matchers = json.loads(response.text)
            for matcher in matchers:
                alignmentEndpoint = "http://localhost:8888/api/alignment"
                logging.info("Alinhando {} e {} usando matcher {}".format(sourceOntology, targetOntology, matcher['name']))
                data = {'ontology1': sourceOntology, 'ontology2': targetOntology, 'matcher': matcher['name'], 'experiment': exp}
                postResponse = requests.post(alignmentEndpoint, data=data)
                if postResponse.status_code in (200,201):
                    logging.info("Alinhamento entre {} e {} executado com sucesso".format(sourceOntology, targetOntology))
                else:
                    print(postResponse.text)
                    logging.error("Falha ao alinhar {} e {}".format(sourceOntology, targetOntology))

    ##Combinar só pares
    ##Combinar ontologias


