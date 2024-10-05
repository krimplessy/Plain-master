import random
import pandas
import xlsxwriter
from ontology.objects import *


class Schedule:
    def __init__(self, planes: [Plane], routes: [Route], cities):
        self.planes = planes
        self.routes = routes
        self.cities = cities

        self.plane_routes = []
        self.df = pandas.DataFrame

        self.time_list = []
        start_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + datetime.timedelta(weeks=1)
        while start_date < end_date:
            self.time_list.append(start_date)
            start_date += datetime.timedelta(minutes=30)

        self.cities_times = {}
        for city in self.cities:
            self.cities_times[city] = self.time_list

    def generate_schedule(self):
        for plane in self.planes:
            # Выбираем допустимые по дальности маршруты
            routes = [route_i for route_i in self.routes if
                      plane.plane_type.plane_distance_min <= route_i.distance <= plane.plane_distance]

            if len(routes) == 0:
                return f'Ошибка связи области знаний и области действительности!\n' \
                       f'Для самолета {plane.plane_name} нет ни одного допустимого маршрута!'
            local_cities_times = {}
            for city in set(route.start_city for route in routes).union(set(route.end_city for route in routes)):
                local_cities_times[city] = self.time_list

            for i in range(len(local_cities_times)):
                for city, city_times in local_cities_times.items():
                    if len(self.plane_routes) != 0 and self.plane_routes[-1].plane.plane_name == plane.plane_name:
                        start_city = self.plane_routes[-1].route.end_city
                        routes = [route_i for route_i in self.routes if
                                  plane.plane_type.plane_distance_min <= route_i.distance <= plane.plane_distance and
                                  route_i.start_city == start_city]
                    potential_routes = []
                    for city_time in city_times:
                        if len(routes) == 0:
                            break
                        route_index = random.randint(0, len(routes) - 1)
                        potential_routes.append(PlaneRoute(plane, routes[route_index], city_time))

                    if len(self.plane_routes) == 0:
                        self.plane_routes.append(potential_routes[0])
                        try:
                            self.cities_times[potential_routes[0].route.start_city].remove(potential_routes[0].start_time)
                            self.cities_times[potential_routes[0].route.end_city].remove(potential_routes[0].end_time)
                        except:
                            pass
                    else:
                        can_append = True
                        for potential_route in potential_routes:
                            for plane_route in self.plane_routes:
                                if plane_route.plane == plane and plane_route.end_time < potential_route.start_time and plane_route.route.end_city == potential_route.route.start_city:
                                    can_append = True
                                elif plane not in [plane_route.plane for plane_route in self.plane_routes]:
                                    can_append = True
                                else:
                                    can_append = False
                            if can_append:
                                self.plane_routes.append(potential_route)
                                try:
                                    self.cities_times[potential_route.route.start_city].remove(potential_route.start_time)
                                    self.cities_times[potential_route.route.end_city].remove(potential_route.end_time)
                                except:
                                    pass

        self.df = pandas.DataFrame(
            columns=['Город отправления', 'Город прибытия', 'Время отправления', 'Время прибытия', 'Самолет',
                     'Тип самолета', 'Дальность полета', 'Дальность маршрута', 'Крейсерская скорость'])
        for plane_route in self.plane_routes:
            self.df.loc[len(self.df)] = [plane_route.route.start_city, plane_route.route.end_city,
                                         plane_route.start_time.strftime("%m-%d %H:%M"),
                                         plane_route.end_time.strftime("%m-%d %H:%M"),
                                         plane_route.plane.plane_name, plane_route.plane.plane_type.plane_type_name,
                                         str(plane_route.plane.plane_type.plane_distance_min) + '-' + str(
                                             plane_route.plane.plane_distance),
                                         plane_route.route.distance, plane_route.plane.plane_speed]
        with pandas.ExcelWriter('schedule.xlsx', engine='xlsxwriter') as writer:
            self.df.to_excel(writer, sheet_name='Расписание 1', index=False)
            # Получаем объект workbook и worksheet
            worksheet = writer.sheets['Расписание 1']
            # Установка максимальной ширины колонки
            for i, col in enumerate(self.df.columns):
                # Для каждой колонки устанавливаем ширину, которая соответствует максимальной длине в строке
                max_width = max(self.df[col].astype(str).map(len).max(), len(col)) + 1
                worksheet.set_column(i, i, max_width)

            self.df = self.df.sort_values(by=['Город отправления', 'Время отправления'])
            self.df.to_excel(writer, sheet_name='Расписание 2', index=False)
            # Получаем объект workbook и worksheet
            worksheet = writer.sheets['Расписание 2']
            # Установка максимальной ширины колонки
            for i, col in enumerate(self.df.columns):
                # Для каждой колонки устанавливаем ширину, которая соответствует максимальной длине в строке
                max_width = max(self.df[col].astype(str).map(len).max(), len(col)) + 1
                worksheet.set_column(i, i, max_width)

        return self.df
