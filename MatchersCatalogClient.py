# This script is reponsible for importing ontologies (and generating profile) of the conference domain into the matchers catalog
import itertools
import json
from os import path
from os import walk
import requests
import csv

## 1) (só se quiser usar as ontologias inteiras)
def import_ontologies():
    matchersCatalogURL = "http://localhost:8888/api/ontologies"
    basepath = "/Users/diegopessoa/Projects/phd/ontologies/conference/"
    ontologias = []
    for (dirpath, dirnames, filenames) in walk(basepath):
        ontologias.extend(list(filter(lambda x: not x.startswith('.') and x.endswith('.owl'), filenames)))
        break  # not recursive

    for ontologia in ontologias:
        filename, file_extension = path.splitext(ontologia)
        json = {'id': filename,
                'description': filename,
                'domain': 'Conference',
                'file': basepath + ontologia,
                'segment': 'false',
                'experiment' : 'exp1'}
        response = requests.post(matchersCatalogURL, json=json)
        if response.status_code in (200, 201):
            print("Ontologia", filename, "importada com sucesso!")

## 1)
def import_ontologies_segments_into_catalog():
    ## TODO ler segmentos de ontologias gerados pelo SOMA para importar no catálogo
    ## Os arquivos estao salvos na pasta local...
    ## Protocolo: source-segment-source-target / target-segment-source-target

    matchersCatalogURL = "http://localhost:8888/api/ontologies"

    # segmentsPath = "/tmp"
    segmentsPath = "/Users/diegopessoa/Projects/phd/soma/experiments/"
    for (dirpath, dirnames, filenames) in walk(segmentsPath):
        files = list(filter(lambda x: x.startswith('source') or x.startswith('target'), filenames))
        break

    expfolders = ['exp2', 'exp3', 'exp4']
    ## TODO varrer cada ontologia de segmento gerado para o experimento e importar no catálogo como ontologia normal para gerar profile.
    for expfolder in expfolders:
        print("************ " + expfolder + " ************")
        segmentPairs = {}
        ontologias = []
        for (dirpath, dirnames, filenames) in walk(segmentsPath + "/" + expfolder):
            ontologias.extend(list(
                filter(lambda x: x.startswith('source') or x.startswith('target') and x.endswith('.owl'), filenames)))
            break

        for file in ontologias:
            type = str(file).split("-")[0]
            source = str(file).split("-")[2]
            target = str(file).split("-")[3].split(".owl")[0]
            index = source + "-" + target
            if not index in segmentPairs:
                segmentPairs[index] = {}
            segmentPairs[index][type] = file
            print(segmentPairs)

        for index in segmentPairs:
            source_file = segmentPairs[index]['source']
            print(source_file)
            target_file = segmentPairs[index]['target']
            print(target_file)

            filename, file_extension = path.splitext(source_file)
            json = {'id': filename,
                    'description': filename,
                    'domain': 'Conference',
                    'file': segmentsPath + "/" + expfolder + "/" + source_file,
                    'segment': 'true',
                    'experiment': expfolder}
            response = requests.post(matchersCatalogURL, json=json)
            if response.status_code in (200, 201):
                print("Segmento (source)", filename, "importado com sucesso!")
            else:
                print("Falha ao importar segmento (source)", filename)

            filename, file_extension = path.splitext(target_file)
            json = {'id': filename,
                    'description': filename,
                    'domain': 'Conference',
                    'file': segmentsPath + "/" + expfolder + "/" + target_file,
                    'segment': 'true',
                    'experiment': expfolder}
            response = requests.post(matchersCatalogURL, json=json)
            if response.status_code in (200, 201):
                print("Segmento (target)", filename, "importado com sucesso!")
            else:
                print("Falha ao importar segmento (target)", filename)

def add_coma_matchers():

    ## Add COMA matcher combinations
    coma_tuples = get_coma_combinations()
    for t in coma_tuples:
        resolution = t[0]
        measure = t[1]
        data = {'name': 'COMA-{}-{}'.format(resolution, measure), 'version': '3.0', 'endPoint': 'http://localhost:8083/api/coma',
                'configurationParameters': {
                    "measure": measure,
                    "resolution": resolution
        }}
        matchersCatalogURL = "http://localhost:8888/api/matcher"
        response = requests.post(matchersCatalogURL, json=data)
        if response.status_code in (200, 201):
            print("matcher ", data['name'], "cadastrado com sucesso")
        else:
            print("Falha ao importar matcher ", data['name'])
            print(response.text)


def add_aml_matchers():
    ## Add AML matcher combinations
    word_combinations, struct_combinations = get_aml_combinations()
    root_path = "/Users/diegopessoa/Projects/phd/matcherscatalog/wrapper-aml/lib/combinations"
    matchersCatalogURL = "http://localhost:8888/api/matcher"

    counter = 1
    for word_comb in word_combinations:
        ##TODO gerar arquivo config
        path = "{}/config-WC-{}.ini".format(root_path,counter)
        config_file_wc = open(path, "w+")
        config_file_wc.write("use_translator=auto\n")
        for tup in word_comb:
            config_file_wc.write(str(tup) + "\n")
        data = {'name': 'AML-WC-{}'.format(counter), 'version': '2.1-SNAPSHOPT',
                'endPoint': 'http://localhost:8084/api/aml',
                'configurationParameters': {
                    "mode": "manual",
                    "bkPath": "aml/knowledge/",
                    "config": "combinations/config-WC-" + str(counter) + ".ini"
                }}
        config_file_wc.close()
        response = requests.post(matchersCatalogURL, json=data)
        if response.status_code in (200, 201):
            print("matcher ", data['name'], "cadastrado com sucesso")
        else:
            print("Falha ao importar matcher ", data['name'])
            print(response.text)
        counter += 1
    counter = 1
    for struct_comb in struct_combinations:
        path = "{}/config-SC-{}.ini".format(root_path, counter)
        config_file_sc = open(path, "w+")
        config_file_sc.write("use_translator=auto\n")
        for tup in struct_comb:
            config_file_sc.write(str(tup) + "\n")
            data = {'name': 'AML-SC-{}'.format(counter), 'version': '2.1-SNAPSHOPT',
                'endPoint': 'http://localhost:8084/api/aml',
                'configurationParameters': {
                    "mode": "manual",
                    "bkPath": "aml/knowledge/",
                    "config": "combinations/config-SC-" + str(counter) + ".ini"
                }}
            response = requests.post(matchersCatalogURL, json=data)
            if response.status_code in (200, 201):
                print("matcher ", data['name'], "cadastrado com sucesso")
            else:
                print("Falha ao importar matcher ", data['name'])
                print(response.text)
            counter += 1
        config_file_sc.close()

def evaluate_alignments_and_generating_profile():
    gold_standard_path = "/Users/diegopessoa/Projects/doutorado/SOMA/gold-standard"

    ## pegar todos os alinhamentos e saber qual o experimento e as ontologias de cada um para usar a validacao...

    ## Pegar todos os alinhamentos agora:
    matchersCatalogURL = "http://localhost:8888/api/alignment"

    response = requests.get(matchersCatalogURL)
    if response.status_code == 200:
        alignments = json.loads(response.text)
        for alignment in alignments:
            ### Generating matching task profile
            response = requests.put(matchersCatalogURL + "/profile/{}".format(alignment['id']))
            if response.status_code == 200:
                sourceOntologyPrefix = alignment['ontology1']['description'].split("-")[2]
                targetOntologyPrefix = alignment['ontology2']['description'].split("-")[3]
                gold_standard = gold_standard_path + "/" + alignment['ontology1']['experiment'] + "/" + sourceOntologyPrefix + "-" + targetOntologyPrefix + ".rdf"
                if path.exists(gold_standard):
                    print("Evaluating alignment with id ", alignment['id'])
                    response = requests.post(matchersCatalogURL + "/evaluations?alignmentId={}&referenceAlignment={}".format(alignment['id'], "file://"+gold_standard))
                    if response.status_code == 200:
                        print("Alinhamento com id ", alignment['id'], "avaliado com sucesso")
                    else:
                        print("Falha ao avaliar alinhamento com id ",alignment['id'])
                        print(response.text)
            else:
                print(response.text)
                print("falha ao gerar profile para alinhamento")
    else:
        print("Falha ao ler alinhamentos")

def get_aml_combinations():
    combinations = []
    bk_sources = ['bk_sources=all', 'bk_sources=none']
    word_matchers = [ 'word_matcher=auto']
    # word_matchers = ['by_class', 'by_name', 'average', 'maximum', 'minimum', 'none', 'auto']
    string_matchers = ['string_matcher=global', 'string_matcher=local', 'string_matcher=none', 'string_matcher=auto']
    string_measures = ['string_measure=ISub','string_measure=Levenstein','string_measure=Jaro-Winkler','string_measure=Q-gram']
    struct_matchers = ['struct_matcher=ancestors','struct_matcher=descendants','struct_matcher=average','struct_matcher=maximum','struct_matcher=minimum','struct_matcher=none','struct_matcher=auto']
    match_properties = ['match_properties=auto']
    # match_properties = ['true', 'false', 'auto']
    selection_types = ['selection_type=auto']
    # selection_types = ['strict', 'permissive', 'hybrid', 'none', 'auto']
    repair_alignments = ['repair_alignment=false']
    # repair_alignments = ['true', 'false']

    word_combinations = list(itertools.product(bk_sources, word_matchers, string_matchers, string_measures, match_properties, selection_types, repair_alignments))
    struct_combinations = list(itertools.product(bk_sources, struct_matchers, match_properties, selection_types, repair_alignments))

    return word_combinations, struct_combinations

def get_coma_combinations():
    tuples = []
    with open('coma-valid-combinations.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            tuples.append(row)
    return tuples