from ontology.objects import *


class OntologyOfReality:
    def __init__(self):
        self.planes = []
        self.routes = []

    def add_plane(self, plane: Plane):
        self.planes.append(plane)

    def add_route(self, route: Route):
        self.routes.append(route)
