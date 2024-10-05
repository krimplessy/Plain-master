import flask
from flask import render_template, request

from app import app
from ontology.main import *
from ontology.objects import PlaneType, Route


@app.route('/', methods=['get'])
def index():
    # refill()
    with open('ontology_of_knowledge.pickle', 'rb') as load_file:
        ontology_of_knowledge = pickle.load(load_file)

    if request.values.get('addCity'):
        ontology_of_knowledge.add_city(request.values.get('city'))
        dump(ontology_of_knowledge=ontology_of_knowledge)
        return flask.redirect(flask.url_for('index'))

    if request.values.get('delCity'):
        ontology_of_knowledge.cities = [city for city in ontology_of_knowledge.cities
                                        if not city == request.values.get('city')]
        dump(ontology_of_knowledge=ontology_of_knowledge)
        return flask.redirect(flask.url_for('index'))

    if request.values.get('addRoute'):
        ontology_of_knowledge.add_route(
            Route(request.values.get('departure'), request.values.get('arrival'), int(request.values.get('distance'))))
        dump(ontology_of_knowledge=ontology_of_knowledge)
        return flask.redirect(flask.url_for('index'))

    if request.values.get('delRoute'):
        ontology_of_knowledge.routes = [route for route in ontology_of_knowledge.routes
                                        if not (route.start_city == request.values.get('departure') and
                                                route.end_city == request.values.get('arrival') and
                                                route.distance == int(request.values.get('distance')))]
        dump(ontology_of_knowledge=ontology_of_knowledge)
        return flask.redirect(flask.url_for('index'))

    if request.values.get('addPlaneType'):
        ontology_of_knowledge.add_plane_type(
            PlaneType(request.values.get('planeType'), int(request.values.get('speedFrom')),
                      int(request.values.get('speedTo')), int(request.values.get('rangeFrom')),
                      int(request.values.get('rangeTo'))))
        dump(ontology_of_knowledge=ontology_of_knowledge)
        return flask.redirect(flask.url_for('index'))

    if request.values.get('delPlaneType'):
        ontology_of_knowledge.plane_types = [
            plane_type for plane_type in ontology_of_knowledge.plane_types
            if not (plane_type.plane_type_name == request.values.get('planeType') and
                    plane_type.plane_speed_min == int(request.values.get('speedFrom')) and
                    plane_type.plane_speed_max == int(request.values.get('speedTo')) and
                    plane_type.plane_distance_min == int(request.values.get('rangeFrom')) and
                    plane_type.plane_distance_max == int(request.values.get('rangeTo')))]
        dump(ontology_of_knowledge=ontology_of_knowledge)
        return flask.redirect(flask.url_for('index'))

    if request.values.get('refill'):
        refill()
        return flask.redirect(flask.url_for('index'))

    cities = ontology_of_knowledge.cities
    routes = ontology_of_knowledge.routes
    plane_types = ontology_of_knowledge.plane_types
    html = render_template(
        'index.html',
        cities=cities,
        routes=routes,
        plane_types=plane_types,
    )
    return html
