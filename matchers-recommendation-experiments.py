## Definir requisito de qualidade para cada cenário.

## Em cada C, critérios diferentes serao utilizados

## Como construir o perfil dos matchers entao?

## 1º Passo: gerar todos os alinhamentos usando os segmentos de cada cenário...

## Preciso carregar todos os alinhamentos

## Gerar valor de qualidade aqui com os pesos para cada requisito

## É fácil filtrar pelas metricas contidas em cada alinhamento
from collections import namedtuple
from pprint import pprint

import requests
import json
from urllib.parse import urlparse
import logging
import math


class OntologyRecommendationParams:
    def __init__(self, ontology1, ontology2, experiment, qualityCriteria):
        self.ontology1 = ontology1
        self.ontology2 = ontology2
        self.experiment = experiment
        self.qualityCriteria = qualityCriteria


class OntologySelectionParams:
    def __init__(self, recommendedMatchers, qualityRequirements):
        self.recommendedMatchers = recommendedMatchers
        self.qualityRequirements = qualityRequirements

def get_recommended_matchers(scenario):
    if scenario == 'c1':
        matchersCatalogUrl = "http://localhost:8888/api/matchers/recommendation"
        qualityCriteria = dict({'precision': 0.7, 'recall': 0.3})
        params = OntologyRecommendationParams("/Users/diegopessoa/Projects/phd/ontologies/conference/cmt.owl",
                                              "/Users/diegopessoa/Projects/phd/ontologies/conference/Conference.owl.",
                                              "exp1", qualityCriteria)
        response = requests.post(matchersCatalogUrl, json=params.__dict__)
        if (response.ok):
            matchers = json.loads(response.text)
            return matchers
        else:
            print(response.text)
            print("nenhum matcher recomendado para este perfil de ontologia")

def get_selected_matchers(scenario):
        matchersCatalogUrl = "http://localhost:8888/api/matchers/selection"
        qualityRequirements = dict( {'qualityMeasure' : 0.3  })
        matchers = get_recommended_matchers(scenario)
        params = OntologySelectionParams(matchers, qualityRequirements)
        response = requests.post(matchersCatalogUrl, json=params.__dict__)
        if (response.ok):
            matchers = json.loads(response.text)
            return matchers
        else:
            print("Falha ao selecionar conjunto final de matchers")

def checkRecommendationAccuracy(exp, metric):
    with open("trainingset/best-matchers/" + exp + "/" + metric + ".json") as file:
        data = json.load(file)

    for key in data:
        value = data[key]
        correctMatcher = value['matcher']
        print("CORRECT MATCHER ="+correctMatcher)
        sourceOntology = value['ontology1']
        targetOntology = value['ontology2']
        print("source ontology = "+sourceOntology)
        print("target ontology = "+targetOntology)

        matchersCatalogUrl = "http://localhost:8888/api/matchers/recommendation"
        qualityCriteria = dict({metric: 1})
        params = OntologyRecommendationParams("/Users/diegopessoa/Projects/phd/SOMA/segments/"+exp+"/"+sourceOntology+".owl",
                                              "/Users/diegopessoa/Projects/phd/SOMA/segments/"+exp+"/"+targetOntology+".owl",
                                              exp, qualityCriteria)
        response = requests.post(matchersCatalogUrl, json=params.__dict__)
        if (response.status_code == 200):
            matchers = json.loads(response.text)
            print("RECOMMENDED MATCHERS = ")
            print(matchers)
        else:
            print("NO MATCHER")


checkRecommendationAccuracy("exp2", "precision")
