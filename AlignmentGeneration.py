import requests
import json
import logging

## 1) Gerar alinhamentos das ontologias/segmentos importados no catálogo para cada matcher.
## 2) Comparar conjunto de treinamento

def exp1_pairs():
    return ['cmt-conference', 'cmt-confOf', 'cmt-edas', 'cmt-ekaw','cmt-iasted', 'cmt-sigkdd', 'conference-confOf', 'conference-edas', 'conference-ekaw', 'conference-iasted', 'conference-sigkdd', 'confOf-edas', 'confOf-ekaw', 'confOf-iasted', 'confOf-sigkdd', 'edas-ekaw', 'edas-iasted', 'edas-sigkdd', 'ekaw-iasted', 'ekaw-sigkdd','iasted-sigkdd']

# Carregar ontologias
def executeAlignments():
    logging.getLogger().setLevel(logging.INFO)
    matchersCatalogURL = "http://localhost:8888/api/ontologies"
    response = requests.get(matchersCatalogURL)
    ontologies = json.loads(response.text)
    ## Executar alinhamento para cada par de ontologia
    ## Fazer combinações...
    # exps = ['exp2', 'exp3', 'exp4']
    exps = ['exp3']
    # exps = ['exp1']
    logging.info("Executando alinhamentos de ontologias")
    for exp in exps:
        logging.info("******************** Alinhando ontologias do experimento {} *********************".format(exp))
        ontologiesToAlign = list(filter(lambda o: o['experiment'] == exp, ontologies))

        alignmentDict = {}

        if exp == 'exp1':
            for sourceOntology in ontologiesToAlign:
                for targetOntology in ontologiesToAlign:
                    pairName = sourceOntology['description']+"-"+targetOntology['description']
                    if sourceOntology == targetOntology or pairName not in exp1_pairs():
                        continue
                    alignmentDict[pairName] = {}
                    alignmentDict[pairName]['source'] = sourceOntology['file']
                    alignmentDict[pairName]['target'] = targetOntology['file']

        else:
            for idx, ontologyToAlign in enumerate(ontologiesToAlign):
                source = str(ontologyToAlign['description']).split("-")[2]
                target = str(ontologyToAlign['description']).split("-")[3].split(".owl")[0]
                # if source == 'cmt' or source == 'conference' or source == 'confOf':
                #     continue
                if not source + '-' + target in alignmentDict:
                    alignmentDict[source + '-' + target] = {}
                if idx % 2 == 0:
                    alignmentDict[source+'-'+target]['source'] = ontologyToAlign['file']
                else:
                    alignmentDict[source+'-'+target]['target'] = ontologyToAlign['file']

        for dic in alignmentDict:
            sourceOntology = alignmentDict[dic]['source']
            targetOntology = alignmentDict[dic]['target']
            matchersEndpoint = "http://localhost:8888/api/matcher"
            response = requests.get(matchersEndpoint)
            matchers = json.loads(response.text)
            for matcher in matchers:
                # if matcher['name'] != 'COMA':
                #     continue
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

executeAlignments()