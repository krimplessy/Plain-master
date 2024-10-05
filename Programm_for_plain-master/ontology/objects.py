import datetime


class PlaneType:
    def __init__(self, plane_type_name, plane_distance_min, plane_distance_max, plane_speed_min, plane_speed_max):
        self.plane_type_name = plane_type_name
        self.plane_distance_min = plane_distance_min
        self.plane_distance_max = plane_distance_max
        self.plane_speed_min = plane_speed_min
        self.plane_speed_max = plane_speed_max


class Plane:
    def __init__(self, plane_name, plane_type: PlaneType, plane_speed, plane_distance):
        self.plane_name = plane_name
        self.plane_type = plane_type
        self.plane_speed = plane_speed
        self.plane_distance = plane_distance


class Route:
    def __init__(self, start_city, end_city, distance):
        self.start_city = start_city
        self.end_city = end_city
        self.distance = distance


class PlaneRoute:
    def __init__(self, plane: Plane, route: Route, start_time: datetime):
        self.plane = plane
        self.route = route
        self.start_time = start_time
        self.end_time = self.start_time + datetime.timedelta(hours=self.route.distance / self.plane.plane_speed)
