from concept import Concept


# A structure to build networks from basic immunology
# classes are organized in a hierarchical structure, although not all possible
# connections may be visualized (that is why we have edges in the graph!)
# definition is used to define the concept, the name field contains the name of
# of the object and may be overriden. The concept also has various numbers of
# connections to other concepts, and may have specific properties, such as alternate
# names, clinical presentations, etc. An object's identity reflects the most specific
# classification. For example, a Neutrophil has the name granulocyte since it is a
# subclass of granulocyte, but it's identity shall be Neuotrophil. Some concepts
# will have associated pictures

# to standardize, most of the classes have 2 parameters that we pass in, but
# occasionally we have a component field. Therefore, when initializing an object
# with a component field we pass in the last 3 arguments

class Generic(Concept):
    def __init__(self, definition, name):
        super().__init__(definition)
        self.name = name

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name


class Generic_Picture(Concept):
    def __init__(self, definition, name):
        super().__init__(definition)
        self.name = name
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name

class Cell(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


# Blood Cells
class HemeStemCell(Cell):
    def __init__(self, definition, name="HemeStemCell"):
        super().__init__(definition, name)


class Mononuclear_Cell(HemeStemCell):
    def __init__(self, definition, name="Mononuclear Cell"):
        super().__init__(definition, name)


class Myeloid(HemeStemCell):
    def __init__(self, definition, name="Myeloid Progenitor"):
        super().__init__(definition, name)
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url


class Granulocyte(Myeloid):
    def __init__(self, definition, identity):
        super().__init__(definition, "Granulocyte")
        self.identity = identity

    def get_name(self):
        return self.name + " " + self.identity


class Thrombocyte(Myeloid):
    def __init__(self, definition, identity):
        super().__init__(definition, "Thrombocyte")
        self.identity = identity

    def get_name(self):
        return self.name + " " + self.identity


class RBC(Myeloid):
    def __init__(self, definition, identity):
        super().__init__(definition, "Red Blood Cell")
        self.identity = identity


class Lymphoid(HemeStemCell):
    def __init__(self, definition, name="Lymphoid Progenitor"):
        super().__init__(definition, name)
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url


class B_Cell(Lymphoid):
    def __init__(self, definition, identity):
        super().__init__(definition, "B-Lymphocyte")
        self.identity = identity

    def get_name(self):
        return self.name + " " + self.identity


class T_Cell(Lymphoid):
    def __init__(self, definition, identity):
        super().__init__(definition, "T-Lymphocyte")
        self.identity = identity

    def get_name(self):
        return self.name + " " + self.identity


# Molecules
class Molecule(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Gene(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Gene")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Cytokine(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Cytokine")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Complement(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Complement")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Antigen(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Antigen")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Antibody(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Antibody")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Receptor(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Receptor")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class MHC_Component(Receptor):
    def __init__(self, definition, identity, component):
        super().__init__(definition, identity)
        self.component = component

    def get_name(self):
        return self.name + " " + self.identity + " " + self.component


class TCR_Component(Receptor):
    def __init__(self, definition, identity, component):
        super().__init__(definition, identity)
        self.component = component

    def get_name(self):
        return self.name + " " + self.identity + " " + self.component


class Antibody_Component(Antibody):
    def __init__(self, definition, identity, component):
        super().__init__(definition, identity)
        self.component = component

    def get_name(self):
        return self.name + " " + self.identity + " " + self.component


class Enzyme(Molecule):
    def __init__(self, definition, identity):
        super().__init__(definition, "Enzyme")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Bond(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Structure(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


# Organs/Structure

class Organ(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Tissue(Organ):
    def __init__(self, definition, identity):
        super().__init__(definition, "Tissue")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Circulatory(Organ):
    def __init__(self, definition, identity, name="Blood Vessel"):
        super().__init__(definition, name)
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Serum(Circulatory):
    def __init__(self, definition, identity):
        super().__init__(definition, identity, "Serum Component")


class Clotting_Factor(Serum, Molecule):
    def __init__(self, definition, identity):
        Serum.__init__(self, definition, identity)
        Molecule.__init__(self, definition, identity)


class Spleen(Circulatory):
    def __init__(self, definition, identity):
        super().__init__(definition, identity, "Spleen Component")


class Skin(Organ):
    def __init__(self, definition, identity):
        super().__init__(definition, "Skin")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Gut(Organ):
    def __init__(self, definition, identity):
        super().__init__(definition, "Gut")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Respiratory(Organ):
    def __init__(self, definition, identity):
        super().__init__(definition, "Respiratory")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class GenitoUrinary(Organ):
    def __init__(self, definition, identity):
        super().__init__(definition, "GenitoUrinary")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Mucosa(Organ):
    def __init__(self, definition, identity):
        super().__init__(definition, "Mucosa")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Lymph(Organ):
    def __init__(self, definition, name="Lymph Tissue"):
        super().__init__(definition, name)


class Gland(Organ):
    def __init__(self, definition, name="Gland"):
        super().__init__(definition, name)


class Malt(Mucosa, Lymph):
    def __init__(self, definition, identity, name="MALT"):
        Lymph.__init__(self, definition, name)
        Mucosa.__init__(self, definition, identity)


class Germinal_Center(Lymph):
    def __init__(self, definition, identity):
        super().__init__(definition, "Germinal Center Tissue")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Central_Lymph(Lymph):
    def __init__(self, definition, identity):
        super().__init__(definition, "Central Lymph Tissue")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Peripheral_Lymph(Lymph):
    def __init__(self, definition, identity):
        super().__init__(definition, "Peripheral Lymph Tissue")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Transplant(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


# Diseases
class Disease(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Hypersensitivity(Disease):
    def __init__(self, definition, identity):
        super().__init__(definition, "Hypersensitivity")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Autoimmune(Disease):
    def __init__(self, definition, identity):
        super().__init__(definition, "Autoimmune Disease")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Immunodeficiency(Disease):
    def __init__(self, definition, identity):
        super().__init__(definition, "Immunodeficient Disease")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Cancer(Disease):
    def __init__(self, definition, identity):
        super().__init__(definition, "Cancer")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Thrombosis(Disease):
    def __init__(self, definition, identity):
        super().__init__(definition, "Thrombosis")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Pathogen(Disease):
    def __init__(self, definition, name="Pathogen"):
        super().__init__(definition, name)


class Bacteria(Pathogen):
    def __init__(self, definition, identity):
        super().__init__(definition, "Bacteria")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Gram_Positive(Bacteria):
    def __init__(self, definition, species):
        super().__init__(definition, "Gram Negative")
        self.species = species

    def get_name(self):
        return self.name + " " + self.identity + " " + self.species


class Gram_Negative(Bacteria):
    def __init__(self, definition, species):
        super().__init__(definition, "Gram Positive")
        self.species = species

    def get_name(self):
        return self.name + " " + self.identity + " " + self.species


class Virus(Pathogen):
    def __init__(self, definition, identity):
        super().__init__(definition, "Virus")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Fungi(Pathogen):
    def __init__(self, definition, identity):
        super().__init__(definition, "Fungi")
        self.picture_url = ""
        self.identity = identity

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


# Symptoms
class Symptom(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Inflammation(Symptom):
    def __init__(self, definition, name="Inflammation"):
        super().__init__(definition, name)
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url


class Attack(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Attack_Molecule(Attack, Molecule):
    def __init__(self, definition, name):
        Molecule.__init__(self, definition, "Lytic Molecule")
        Attack.__init__(self, definition, name)


# Lab
class Lab(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Serologic_Test(Lab):
    def __init__(self, definition, name="Generic Serologic Test"):
        super().__init__(definition, name)


class Coagulation(Lab):
    def __init__(self, definition, name="Generic Coagulation test"):
        super().__init__(definition, name)


# Treatments
class Treatment(Generic):
    def __init__(self, definition, name):
        super().__init__(definition, name)


class Immunotherapy(Treatment):
    def __init__(self, definition, identity):
        super().__init__(definition, "Immunotherapy")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Antimicrobial(Treatment):
    def __init__(self, definition, identity):
        super().__init__(definition, "Antimicrobial Agent")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Drug(Treatment):
    def __init__(self, definition, identity):
        super().__init__(definition, "Drug")
        self.identity = identity
        self.picture_url = ""

    def set_picture(self, url):
        self.picture_url = url

    def get_picture(self):
        return self.picture_url

    def get_name(self):
        return self.name + " " + self.identity


class Transplant_Drug(Drug):
    def __init__(self, definition, identity="Transplant Pharmacotherapy"):
        super().__init__(definition, identity)


class Anti_Inflammatory_Drug(Drug):
    def __init__(self, definition, identity="Anti-Inflammatory Pharmacotherapy"):
        super().__init__(definition, identity)

# Responses will just create generic concepts(immunogeneicity, adaptive and innate immunity)
# Humoral immunity, Cell mediated Immunity
