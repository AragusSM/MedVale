from .concept import *


# A structure to build networks from basic microbiology
# classes are organized in a hierarchical structure, although not all possible
# connections may be visualized (that is why we have edges in the graph!)
# definition is used to define the concept, the name field contains the name of
# of the object and may be overriden. The concept also has various numbers of
# connections to other concepts, and may have specific properties, such as alternate
# names, clinical presentations, etc. An object's identity reflects the most specific
# classification.
# to standardize, We have a generic class of pathogen, with specific subclasses based on
# pathogen properties.
# We will also just use the generic class for everything not antimicobial or pathogen related

class Generic(Concept):
    def __init__(self, identity, definition, name):
        super().__init__(identity, definition)
        self.name = name
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name


class Cell_Structure(Generic):
    def __init__(self, identity, definition, name):
        super().__init__(identity, definition, name)


class Lab(Generic):
    def __init__(self, identity, definition, name):
        super().__init__(identity, definition, name)


class Clinical(Generic):
    def __init__(self, identity, definition, name):
        super().__init__(identity, definition, name)


class Disease(Generic):
    def __init__(self, identity, definition, name):
        super().__init__(identity, definition, name)


class Pathogen(Generic):
    def __init__(self, identity, definition, name="Pathogen"):
        super().__init__(identity, definition, name)


# For bacteria, gram can either be +, -, or indeterminate
class Bacteria(Pathogen):
    def __init__(self, identity, definition, gram, name="Bacteria"):
        super().__init__(identity, definition, name)
        self.gram_type = gram  # Specific attribute for Bacteria


class Coccus(Bacteria):
    def __init__(self, identity, definition, gram, name="Cocci"):
        super().__init__(identity, definition, gram, name)


class Bacillus(Bacteria):
    def __init__(self, identity, definition, gram, name="Bacilli"):
        super().__init__(identity, definition, gram, name)


class Branched_Rods(Bacteria):
    def __init__(self, identity, definition, gram, name="Branched Rods"):
        super().__init__(identity, definition, gram, name)


class Mycobacteria(Bacteria):
    def __init__(self, identity, definition, gram, name="Mycobacteria"):
        super().__init__(identity, definition, gram, name)


class Coccobacillus(Bacteria):
    def __init__(self, identity, definition, gram, name="Coccobacillus"):
        super().__init__(identity, definition, gram, name)


class Spirochete(Bacteria):
    def __init__(self, identity, definition, gram, name="Spirochetes"):
        super().__init__(identity, definition, gram, name)


class Fungus(Pathogen):
    def __init__(self, identity, definition, name="Fungus"):
        super().__init__(identity, definition, name)


class Virus(Pathogen):
    def __init__(self, identity, definition, gene_material, name="Virus"):
        super().__init__(identity, definition, name)
        self.gene_material = gene_material  # Specific attribute for Virus


class PositiveSenseRNA(Virus):
    def __init__(self, identity, definition, gene_material, name="PositiveSenseRNAVirus"):
        super().__init__(identity, definition, gene_material, name)


class NegativeSenseRNA(Virus):
    def __init__(self, identity, definition, gene_material, name="NegativeSenseRNAVirus"):
        super().__init__(identity, definition, gene_material, name)


class DNAVirus(Virus):
    def __init__(self, identity, definition, gene_material, name="DNAVirus"):
        super().__init__(identity, definition, gene_material, name)


class Parasite(Pathogen):
    def __init__(self, identity, definition, name="Parasite"):
        super().__init__(identity, definition, name)


class Antimicrobial(Generic):
    def __init__(self, identity, definition, name="Antimicrobial"):
        super().__init__(identity, definition, name)


class Antibacterial(Antimicrobial):
    def __init__(self, identity, definition, name="Antibacterial"):
        super().__init__(identity, definition, name)


class Beta_Lactam(Antibacterial):
    def __init__(self, identity, definition, name="Beta_Lactam"):
        super().__init__(identity, definition, name)


class Cephalosporin(Beta_Lactam):
    def __init__(self, identity, definition, name="Cephalosporin"):
        super().__init__(identity, definition, name)


class Carbapenem(Beta_Lactam):
    def __init__(self, identity, definition, name="Carbapenem"):
        super().__init__(identity, definition, name)


class Tetracycline(Antibacterial):
    def __init__(self, identity, definition, name="Tetracyline"):
        super().__init__(identity, definition, name)


class Antimycobacterial(Antibacterial):
    def __init__(self, identity, definition, name="Antimycobacterial"):
        super().__init__(identity, definition, name)


class Antifungal(Antimicrobial):
    def __init__(self, identity, definition, name="Antifungal"):
        super().__init__(identity, definition, name)


class HIV_Antiviral(Antimicrobial):
    def __init__(self, identity, definition, name="HIV Antiviral"):
        super().__init__(identity, definition, name)


class Antiviral(Antimicrobial):
    def __init__(self, identity, definition, name="Antiviral"):
        super().__init__(identity, definition, name)


class Antiparasite(Antimicrobial):
    def __init__(self, identity, definition, name="Antiparasite"):
        super().__init__(identity, definition, name)
