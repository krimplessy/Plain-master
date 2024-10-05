import pandas

from ontology.objects import *
from ontology.ontology_of_knowledge import OntologyOfKnowledge
from ontology.ontology_of_reality import OntologyOfReality
from ontology.schedule import Schedule
import pickle


def Check(ook: OntologyOfKnowledge, oor: OntologyOfReality):
    # Проверяем область знаний
    check_result = ''
    if len(ook.cities) < 2:
        check_result += f'Ошибка в области знаний! Количество городов: {len(ook.cities)} < 2.\n'
    else:
        for i in range(len(ook.cities) - 1):
            for j in range(i + 1, len(ook.cities)):
                if ook.cities[i] == ook.cities[j]:
                    check_result += f'Ошибка в области знаний! Город {ook.cities[i]} дублируется.\n'

    if len(ook.routes) == 0:
        check_result += f'Ошибка в области знаний! Маршруты не заданы!\n'
    for i in range(len(ook.routes) - 1):
        for j in range(i + 1, len(ook.routes)):
            if ook.routes[i].start_city == ook.routes[j].start_city \
                    and ook.routes[i].end_city == ook.routes[j].end_city \
                    and ook.routes[i].distance == ook.routes[j].distance:
                check_result += f'Ошибка в области знаний! Марушрут {ook.routes[i].start_city} -> ' \
                                f'{ook.routes[i].end_city} {ook.routes[i].distance} дублируется.\n'
    for route in ook.routes:
        if route.start_city not in ook.cities:
            check_result += f'Ошибка в области знаний! Город {route.start_city} не входит в множество городов: {ook.cities} ' \
                            f'(маршрут {route.start_city} -> {route.end_city} {route.distance}).\n'
        if route.end_city not in ook.cities:
            check_result += f'Ошибка в области знаний! Город {route.end_city} не входит в множество городов: {ook.cities} ' \
                            f'(маршрут {route.start_city} -> {route.end_city} {route.distance}).\n'
        if route.start_city == route.end_city:
            check_result += f'Ошибка в области знаний! Начало маршрута = конец маршрута ({route.start_city} = {route.end_city}) ' \
                            f'(маршрут {route.start_city} -> {route.end_city} {route.distance}).\n'
        if route.distance == 0:
            check_result += f'Ошибка в области знаний! Для маршрута {route.start_city} -> {route.end_city} дальность маршрута = 0.\n'

    if len(ook.routes) == 0:
        check_result += f'Ошибка в области знаний! Типы самолетов не заданы!\n'
    for i in range(len(ook.plane_types) - 1):
        for j in range(i + 1, len(ook.plane_types)):
            if ook.plane_types[i].plane_type_name == ook.plane_types[j].plane_type_name \
                    or ook.plane_types[i].plane_distance_min == ook.plane_types[j].plane_distance_min \
                    and ook.plane_types[i].plane_distance_max == ook.plane_types[j].plane_distance_max \
                    and ook.plane_types[i].plane_speed_min == ook.plane_types[j].plane_speed_min \
                    and ook.plane_types[i].plane_speed_max == ook.plane_types[j].plane_speed_max:
                check_result += f'Ошибка в области знаний! Тип самолета "{ook.plane_types[i].plane_type_name}" дублируется.\n'
    for plane_type in ook.plane_types:
        if plane_type.plane_speed_min > plane_type.plane_speed_max:
            check_result += f'Ошибка в области знаний! Для типа самолета {plane_type}' \
                            f' минимальная крейсерская скорость > максимальной крейсерской скорости:' \
                            f' {plane_type.plane_speed_min} > {plane_type.plane_speed_max}.\n'
        if plane_type.plane_distance_min > plane_type.plane_distance_max:
            check_result += f'Ошибка в области знаний! Для типа самолета {plane_type}' \
                            f' минимальная дальность полета > максимальной дальности полета:' \
                            f' {plane_type.plane_distance_min} > {plane_type.plane_distance_max}.\n'

    # Проверяем область действительности
    if len(oor.planes) == 0:
        check_result += f'Ошибка в области действительности! самолета не заданы.\n'

    if len(oor.routes) == 0:
        check_result += f'Ошибка в области действительности! Маршруты не заданы.\n'
    for i in range(len(oor.routes) - 1):
        for j in range(i + 1, len(oor.routes)):
            if oor.routes[i].start_city == oor.routes[j].start_city \
                    and oor.routes[i].end_city == oor.routes[j].end_city \
                    and oor.routes[i].distance == oor.routes[j].distance:
                check_result += f'Ошибка в области действительности! Марушрут {oor.routes[i].start_city} -> ' \
                                f'{oor.routes[i].end_city} {oor.routes[i].distance} дублируется.\n'

    for i in range(len(oor.planes) - 1):
        for j in range(i + 1, len(oor.planes)):
            if oor.planes[i].plane_name == oor.planes[j].plane_name:
                check_result += f'Ошибка в области действительности! самолет {oor.planes[i].plane_name} дублируется.\n'

    for plane in oor.planes:
        if plane.plane_distance < plane.plane_type.plane_distance_min:
            check_result += f'Ошибка в области действительности! Для самолета {plane.plane_name}' \
                            f' дальность полета < минимальной дальности полета для заданного типа ' \
                            f'({plane.plane_type.plane_type_name}): {plane.plane_distance} < {plane.plane_type.plane_distance_min}.\n'
        if plane.plane_distance > plane.plane_type.plane_distance_max:
            check_result += f'Ошибка в области действительности! Для самолета {plane.plane_name}' \
                            f' дальность полета > максимальной дальности полета для заданного типа ' \
                            f'({plane.plane_type.plane_type_name}): {plane.plane_distance} > {plane.plane_type.plane_distance_max}.\n'
        if plane.plane_speed < plane.plane_type.plane_speed_min:
            check_result += f'Ошибка в области действительности! Для самолета {plane.plane_name}' \
                            f' дальность полета < минимальной крейсерской скорости для заданного типа ' \
                            f'({plane.plane_type.plane_type_name}): {plane.plane_speed} < {plane.plane_type.plane_speed_min}.\n'
        if plane.plane_speed > plane.plane_type.plane_speed_max:
            check_result += f'Ошибка в области действительности! Для самолета {plane.plane_name}' \
                            f'Крейсерская скорость > максимальной крейсерской скорости для заданного типа ' \
                            f'({plane.plane_type.plane_type_name}): {plane.plane_speed} > {plane.plane_type.plane_speed_max}.\n'

    # Проверяем связи
    for plane in oor.planes:
        if plane.plane_type.plane_type_name not in [plane_type.plane_type_name for plane_type in ook.plane_types]:
            check_result += f'Ошибка связи области знаний и области действительности! Неизвестный тип {plane.plane_type.plane_type_name}' \
                            f' для самолета {plane.plane_name}.\n'

    if check_result:
        return check_result
    else:
        return 0


def refill():
    ontology_of_knowledge = OntologyOfKnowledge()
    ontology_of_reality = OntologyOfReality()
    
    ontology_of_knowledge.add_plane_type(PlaneType('дальнемагистральное дозвуковое воздушное судно', 6000, 20000, 600, 800))
    ontology_of_knowledge.add_plane_type(PlaneType('дальнемагистральное трансзвуковое воздушное судно', 6000, 20000, 800, 1200))
    ontology_of_knowledge.add_plane_type(PlaneType('дальнемагистральное сверхзвуковое воздушное судно', 6000, 20000, 1200, 2000))
    ontology_of_knowledge.add_plane_type(PlaneType('среднемагистральное дозвуковое воздушное судно', 1000, 6000, 600, 800))
    ontology_of_knowledge.add_plane_type(PlaneType('среднемагистральное трансзвуковое воздушное судно', 1000, 6000, 800, 1200))
    ontology_of_knowledge.add_plane_type(PlaneType('среднемагистральное сверхзвуковое воздушное судно', 1000, 6000, 1200, 2000))
    ontology_of_knowledge.add_plane_type(PlaneType('дозвуковое воздушное судно местных авиалиний', 400, 1000, 600, 800))
    ontology_of_knowledge.add_plane_type(PlaneType('трансзвуковое воздушное судно местных авиалиний', 400, 1000, 800, 1200))
    ontology_of_knowledge.add_plane_type(PlaneType('сверхзвуковое воздушное судно местных авиалиний', 400, 1000, 1200, 2000))

    ontology_of_knowledge.add_city('Владивосток')
    ontology_of_knowledge.add_city('Красноярск')
    ontology_of_knowledge.add_city('Хабаровск')
    ontology_of_knowledge.add_city('Москва')
    ontology_of_knowledge.add_city('Магадан')

    ontology_of_knowledge.add_route(Route('Владивосток', 'Красноярск', 4000))
    ontology_of_knowledge.add_route(Route('Хабаровск', 'Красноярск', 3100))
    ontology_of_knowledge.add_route(Route('Москва', 'Владивосток', 9000))
    ontology_of_knowledge.add_route(Route('Хабаровск', 'Владивосток', 960))
    ontology_of_knowledge.add_route(Route('Магадан', 'Владивосток', 2400))
    ontology_of_knowledge.add_route(Route('Москва', 'Хабаровск', 7200))

    ontology_of_knowledge.add_route(Route('Красноярск', 'Владивосток', 4000))
    ontology_of_knowledge.add_route(Route('Красноярск', 'Хабаровск', 3100))
    ontology_of_knowledge.add_route(Route('Владивосток', 'Москва', 9000))
    ontology_of_knowledge.add_route(Route('Владивосток', 'Хабаровск', 960))
    ontology_of_knowledge.add_route(Route('Владивосток', 'Магадан', 2400))
    ontology_of_knowledge.add_route(Route('Хабаровск', 'Москва', 7200))

    ontology_of_reality.routes = ontology_of_knowledge.routes

    ontology_of_reality.add_plane(Plane('A000', ontology_of_knowledge.plane_types[0], 700, 9000))
    ontology_of_reality.add_plane(Plane('A001', ontology_of_knowledge.plane_types[0], 790, 7300))
    ontology_of_reality.add_plane(Plane('A002', ontology_of_knowledge.plane_types[1], 1000, 7200))
    ontology_of_reality.add_plane(Plane('A003', ontology_of_knowledge.plane_types[2], 1350, 9000))
    ontology_of_reality.add_plane(Plane('A004', ontology_of_knowledge.plane_types[2], 1200, 8000))
    ontology_of_reality.add_plane(Plane('A005', ontology_of_knowledge.plane_types[3], 700, 4600))
    ontology_of_reality.add_plane(Plane('A006', ontology_of_knowledge.plane_types[4], 900, 3000))
    ontology_of_reality.add_plane(Plane('A007', ontology_of_knowledge.plane_types[5], 1250, 5600))
    ontology_of_reality.add_plane(Plane('A008', ontology_of_knowledge.plane_types[6], 650, 970))
    ontology_of_reality.add_plane(Plane('A009', ontology_of_knowledge.plane_types[7], 870, 1000))

    dump(ontology_of_knowledge, ontology_of_reality)


def dump(ontology_of_knowledge=None, ontology_of_reality=None, schedule=None):
    if ontology_of_knowledge is not None:
        with open('ontology_of_knowledge.pickle', 'wb+') as dump_file:
            pickle.dump(ontology_of_knowledge, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
    if ontology_of_reality is not None:
        with open('ontology_of_reality.pickle', 'wb+') as dump_file:
            pickle.dump(ontology_of_reality, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
    if schedule is not None:
        with open('schedule.pickle', 'wb+') as dump_file:
            pickle.dump(schedule, dump_file, protocol=pickle.HIGHEST_PROTOCOL)


def call_gen_schedule(ontology_of_knowledge: OntologyOfKnowledge, ontology_of_reality: OntologyOfReality):
    check = Check(ontology_of_knowledge, ontology_of_reality)
    if check == 0:
        schedule = Schedule(ontology_of_reality.planes, ontology_of_reality.routes, ontology_of_knowledge.cities)
        schedule_result = schedule.generate_schedule()
        # if type(schedule_result) != pandas.DataFrame:
        #     return schedule_result
        # with open('schedule.pickle', 'wb') as dump_file:
        #     pickle.dump(schedule, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
        return schedule_result
    else:
        return check
