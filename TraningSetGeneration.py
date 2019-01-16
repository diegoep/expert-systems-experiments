import itertools

from sklearn import tree
from sklearn.datasets import load_iris
import graphviz
import requests
import json
import csv

def generate_training_sets(minvalue, metric, experiment, maxQuantity):
    matchersCatalogUrl = "http://localhost:8888/api/alignment/find-by-metric"
    response = requests.get(matchersCatalogUrl + "?minValue={}&metric={}&experiment={}&quantity={}".format(minvalue, metric, experiment, maxQuantity))
    if response.status_code == 200:
        alignments = json.loads(response.text)

        trainingSet = []

        for alignment in alignments:
            trainingSetEntry = {}
            trainingSetEntry['lexicalMetricsAfinity'] = alignment['alignmentProfile']['metrics']['lexicalMetricsAfinity']
            trainingSetEntry['syntacticMetricsAfinity'] = alignment['alignmentProfile']['metrics']['syntacticMetricsAfinity']
            trainingSetEntry['structuralMetricsAfinity'] = alignment['alignmentProfile']['metrics']['structuralMetricsAfinity']
            trainingSetEntry['matcher'] = alignment['matcher']['name']
            trainingSetEntry[metric] = alignment['alignmentEvaluation']['metrics'][metric]
            trainingSet.append(trainingSetEntry)

        keys = trainingSet[0].keys()
        with open("trainingset/training-{}.csv".format(metric), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, keys)
            writer.writeheader()
            writer.writerows(trainingSet)
    else:
        print("falha ao ler alinhamentos no catálogo")
        print(response.text)

def generate_training_sets_old(minvalue, metric):
    matchersCatalogUrl = "http://localhost:8888/api/alignment/find-by-metric"
    response = requests.get(matchersCatalogUrl + "?minvalue={}&metric={}".format(minvalue, metric))
    if (response.status_code == 200):
        alignments = json.loads(response.text)

        trainingSet = []
        for alignment in alignments:
            trainingSetEntry = {}
            trainingSetEntry['avgDepth'] = alignment['matchingTaskProfile']['metrics']['avgDepth']
            trainingSetEntry['relationshipRichness'] = alignment['matchingTaskProfile']['metrics']['relationshipRichness']
            trainingSetEntry['attributeRichness'] = alignment['matchingTaskProfile']['metrics']['attributeRichness']
            trainingSetEntry['inheritanceRichness'] = alignment['matchingTaskProfile']['metrics']['inheritanceRichness']
            trainingSetEntry['labelWordnet'] = alignment['matchingTaskProfile']['metrics']['labelWordnet']
            trainingSetEntry['localWordnet'] = alignment['matchingTaskProfile']['metrics']['localWordnet']
            trainingSetEntry['classRichness'] = alignment['matchingTaskProfile']['metrics']['classRichness']
            trainingSetEntry['avgPopulation'] = alignment['matchingTaskProfile']['metrics']['avgPopulation']
            trainingSetEntry['nullCommentPerc'] = alignment['matchingTaskProfile']['metrics']['nullCommentPerc']
            trainingSetEntry['nullLabelPerc'] = alignment['matchingTaskProfile']['metrics']['nullLabelPerc']
            trainingSetEntry['labelUniqueness'] = alignment['matchingTaskProfile']['metrics']['labelUniqueness']
            trainingSetEntry[metric] = alignment['alignmentEvaluation']['metrics'][metric]
            trainingSetEntry['matcher'] = alignment['matcher']['name']
            if not any (d['avgDepth'] == trainingSetEntry['avgDepth']
                        and d['relationshipRichness'] == trainingSetEntry['relationshipRichness']
                        and d['attributeRichness'] == trainingSetEntry['attributeRichness']
                        and d['inheritanceRichness'] == trainingSetEntry['inheritanceRichness']
                        and d['labelWordnet'] == trainingSetEntry['labelWordnet']
                        and d['localWordnet'] == trainingSetEntry['localWordnet']
                        and d['classRichness'] == trainingSetEntry['classRichness']
                        and d['avgPopulation'] == trainingSetEntry['avgPopulation']
                        and d['nullCommentPerc'] == trainingSetEntry['nullCommentPerc']
                        and d['nullLabelPerc'] == trainingSetEntry['nullLabelPerc']
                        and d['labelUniqueness'] == trainingSetEntry['labelUniqueness']
                        and d[metric] == trainingSetEntry[metric]
                        for d in trainingSet):
                trainingSet.append(trainingSetEntry)
        keys = trainingSet[0].keys()
        with open("trainingset/training-{}.csv".format(metric), 'w') as csvfile:
            writer = csv.DictWriter(csvfile, keys)
            writer.writeheader()
            writer.writerows(trainingSet)
    else:
        print("falha ao ler alinhamentos no catálogo")
        print(response.text)

def generate_afinity_combinations():
    afinityMetrics = ['lexical', 'structural', 'syntactic']
    afinityMetricsValues = ['LOW', 'MEDIUM', 'HIGH']
    qualityMeasures = [['precision'], ['recall'], ['fmeasure'], ['executionTime']]

    afinityValues = list(itertools.product(afinityMetricsValues, repeat=3))

    combinations = list(itertools.product(afinityValues, qualityMeasures))

    flatList = list(itertools.chain(*combinations))
    print(flatList)

    keys = ['lexicalAfinity', 'structuralAfinity', 'syntacticAfinity', 'measure']

    with open("trainingset/combinations.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(flatList)

def find_best_matchers(minValue, metric, experiment):
    matchersCatalogUrl = "http://localhost:8888/api/alignment/find-by-metric"
    response = requests.get(
        matchersCatalogUrl + "?minValue={}&metric={}&experiment={}&quantity={}".format(minValue, metric, experiment, 1))
    if response.status_code == 200:
        alignments = json.loads(response.text)
        print(alignments)
        bestMatchers = []
        for alignment in alignments:
            bestMatcherEntry = {}
            bestMatcherEntry['ontology1'] = alignment['ontology1']['description']
            bestMatcherEntry['ontology2'] = alignment['ontology2']['description']
            bestMatcherEntry['matcher'] = alignment['matcher']['name']
            bestMatchers.append(bestMatcherEntry)

        with open("trainingset/best-matchers.csv", 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ontology1', 'ontology2', 'matcher'])
            writer.writerows(bestMatchers)

find_best_matchers(0.3, "precision", "exp2")
