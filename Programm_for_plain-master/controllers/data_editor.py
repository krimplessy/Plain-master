import flask
from flask import render_template, request

from app import app
from ontology.main import *


@app.route('/data_editor', methods=['get'])
def data_editor():
    refill()
    with open('ontology_of_knowledge.pickle', 'rb') as load_file:
        ontology_of_knowledge = pickle.load(load_file)
    with open('ontology_of_reality.pickle', 'rb') as load_file:
        ontology_of_reality = pickle.load(load_file)

    all_routes = ontology_of_knowledge.routes
    plane_types = ontology_of_knowledge.plane_types
    planes = ontology_of_reality.planes
    current_routes = ontology_of_reality.routes

    if request.values.get('addTravelTrip'):
        ontology_of_reality.add_route(ontology_of_knowledge.routes[int(request.values.get('route'))])
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    if request.values.get('delTravelTrip'):
        del_route = ontology_of_knowledge.routes[int(request.values.get('route'))]
        ontology_of_reality.routes = [route for route in ontology_of_reality.routes
                                      if not (route.start_city == del_route.start_city and
                                              route.end_city == del_route.end_city and
                                              route.distance == del_route.distance)]
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    if request.values.get('addPlane'):
        ontology_of_reality.add_plane(Plane(request.values.get('plane-number'),
                                            ontology_of_knowledge.plane_types[int(request.values.get('plane-type'))],
                                            int(request.values.get('speed')),
                                            int(request.values.get('distance'))))
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    if request.values.get('delPlane'):
        ontology_of_reality.planes = [plane for plane in ontology_of_reality.planes
                                      if not (plane.plane_name == request.values.get('plane-number') and
                                              plane.plane_type.plane_type_name == ontology_of_knowledge.plane_types[
                                                  int(request.values.get('plane-type'))].plane_type_name and
                                              plane.plane_distance == int(request.values.get('distance')) and
                                              plane.plane_speed == int(request.values.get('speed')))]
        dump(ontology_of_reality=ontology_of_reality)
        return flask.redirect(flask.url_for('data_editor'))

    html = render_template(
        'data_editor.html',
        len=len,
        int=int,
        plane_types=plane_types,
        all_routes=all_routes,
        planes=planes,
        current_routes=current_routes
    )

    return html
