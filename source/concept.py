class Concept:
    def __init__(self, identity, definition):
        self.identity = identity
        self.definition = definition
        self.properties = []
        self.connections = []  # List to hold connections

    def add_connection(self, connection_type, child_concept):
        # Add a new connection to the list
        connection = Connection(connection_type, self, child_concept)
        self.connections.append(connection)

    def add_property(self, property):
        self.properties.append(property)

    def __repr__(self):
        return f"Concept(definition='{self.definition}')"

    def get_def(self):
        return self.definition


class Connection:
    def __init__(self, connection_type, parent, child):
        self.connection_type = connection_type
        self.connection_desc = ""
        self.parent = parent
        self.child = child

    def get_connection(self):
        return self.connection_type

    def get_parent(self):
        return self.parent

    def get_child(self):
        return self.child

    def get_desc(self):
        return self.connection_desc

    def set_desc(self, desc):
        self.connection_desc = desc

    def __repr__(self):
        return f"Connection(type='{self.connection_type}', parent={self.parent.name}, child={self.child.name})"



# # Example usage
# concept1 = Concept("Photosynthesis")
# concept2 = Concept("Sunlight")
# concept3 = Concept("Chlorophyll")
#
# # Adding connections
# concept1.add_connection("requires", concept2)
# concept1.add_connection("involves", concept3)
#
# # Accessing connections
# print(concept1.connections)