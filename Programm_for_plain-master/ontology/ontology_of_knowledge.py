from ontology.objects import *


class OntologyOfKnowledge:
    def __init__(self):
        self.plane_types = []
        self.cities = []
        self.routes = []

    def add_city(self, city):
        self.cities.append(city)

    def add_route(self, route: Route):
        self.routes.append(route)

    def add_plane_type(self, plane_type: PlaneType):
        self.plane_types.append(plane_type)
