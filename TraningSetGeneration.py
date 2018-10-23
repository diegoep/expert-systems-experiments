from sklearn import tree
from sklearn.datasets import load_iris
import graphviz
import requests
import json
import csv

def generate_training_sets(minvalue, metric):
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

generate_training_sets(0.5, "recall")