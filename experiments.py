## Reorganizar experimentos em um único arquivo para ser a chamada.

from MatchersCatalogClient import *
from OntologiesCatalogClient import *
from AlignmentGeneration import *

class Experiments:

    def __init__(self):
        pass

    def preparation(self):
        ## Import Whole ontologies:
        import_ontologies()

        ## Import ontologies in ontology catalog for generating segments
        import_ontologies_into_catalog()

        ## Import segments
        import_ontologies_segments_into_catalog()

        ## Calculate matching task profiling (combination of source and target ontology profiles)


        ## Add COMA Matchers combination
        add_coma_matchers()

        ## Add AML matchers combination
        add_aml_matchers()

        ## Run alingments for each matcher generated
        executeAlignments()



    def execution(self):
        ## Evaluate alignments and generating profile
        evaluate_alignments_and_generating_profile()

exp = Experiments()
exp.execution()





