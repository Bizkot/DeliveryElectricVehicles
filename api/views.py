from django.http import HttpResponse
import csv
import io
import numpy
import configparser
import datetime

from django.views.decorators.csrf import csrf_exempt

from api.Visit import Visit
from api.Vehicle import Vehicle
from api.VisitLinkedList import Node, VisitLinkedList

@csrf_exempt
def index(request):
    urls = []
    urls.append('api/firstheuristic')
    urls.append('api/secondheuristic')
    return HttpResponse('\n'.join(urls))


@csrf_exempt
def first_heuristic(request):
    if request.method == 'POST':
        if request.FILES:
            visits_file = request.FILES.get('visits')
            distance_file = request.FILES.get('distance')
            times_file = request.FILES.get('times')
            vehicle_config_file = request.FILES.get('vehicle')

            visits = load_visits(visits_file)
            distances = load_distances(distance_file)
            times = load_times(times_file)
            vehicle = load_vehicle_config(vehicle_config_file)
            possible_visit_list = define_visit_order(
                vehicle, distances, times, visits)
            return HttpResponse(possible_visit_list)
        else:
            return HttpResponse("Files not found")
    else:
        return HttpResponse("Wrong method")


def load_visits(visits_file):
    """Return a Visit array

    Parameters:
    visits_file: CSV file representing visits for a day
    """
    decoded_visits_file = visits_file.read().decode('latin-1')
    io_string = io.StringIO(decoded_visits_file)
    line_count = 0
    visits = []
    for visit in csv.reader(io_string, delimiter=',', quotechar='|'):
        if line_count == 0:
            pass
        else:
            # visit[0] = visit_id; visit[1] = visit_name; visit[2] = visit_lat; visit[3] = visit_lon; visit[4] = demand
            visits.append(Visit(int(visit[0]), visit[1],
                                float(visit[2]), float(visit[3]), int(visit[4])))
        line_count += 1
    return visits


def load_distances(distance_file):
    """Return a distance matrix

    Parameters:
    distance_file: Text file representing distances between locations
    """
    distances = numpy.loadtxt(distance_file)
    return distances


def load_times(time_file):
    """Return a time matrix

    Parameters:
    time_file: Text file representing time between locations
    """
    times = numpy.loadtxt(time_file)
    return times


def load_vehicle_config(vehicle_config_file):
    """Return a Vehicle

    Parameters:
    vehicle_config_file: Ini file with vehicle config
    """
    vehicle_config = configparser.ConfigParser()
    vehicle_config.read(vehicle_config_file)
    # vehicle = Vehicle(vehicle_config.get('Vehicle', 'max_dist'), vehicle_config.get('Vehicle', 'capacity'),
    #                   vehicle_config.get('Vehicle', 'charge_fast'), vehicle_config.get('Vehicle', 'charge_medium'),
    #                   vehicle_config.get('Vehicle', 'charge_slow'), vehicle_config.get('Vehicle', 'start_time'),
    #                   vehicle_config.get('Vehicle', 'end_time'))
    # Can't read properly the vehicle.ini file, so hard coding the vehicle config
    vehicle = Vehicle(150, 100, 60, 180, 480, '07:00', '19:00')
    return vehicle


def get_distance(distances, origin, destination):
    """Return the distance between two locations

    Parameters:
    distances: Distance matrix
    origin: Origin id
    destination: Destination id
    """
    return distances.item((origin, destination))


def get_time(times, origin, destination):
    """Return the time between two locations

    Parameters:
    times: Time matrix
    origin: Origin id
    destination: Destination id
    """
    return times.item((origin, destination))


def has_enough_energy(vehicle, distances, origin, destination):
    """Return true if the vehicle has enough energy to reach its next location and then go back to the depot

    Parameters:
    vehicle: The vehicle
    distances: Distance matrix
    origin: Origin id
    destination: Destination id
    """
    next_visit_distance = get_distance(distances, origin, destination)
    # Depot id is always 0
    back_to_depot_distance = get_distance(distances, destination, 0)
    total_distance = next_visit_distance + back_to_depot_distance
    return vehicle.dist_left >= total_distance


def has_enough_time(vehicle, times, origin, destination):
    """Return true if the vehicle has enough time to reach its next location and then go back to the depot

    Parameters:
    vehicle: The vehicle
    times: Time matrix
    origin: Origin id
    destination: Destination id
    """
    next_visit_time = get_time(times, origin, destination)
    # Depot id is always 0
    back_to_depot_time = get_time(times, origin, destination)
    total_time_seconds = next_visit_time + back_to_depot_time
    total_time = datetime.timedelta(seconds=total_time_seconds)
    return vehicle.working_time_left >= total_time


def has_enough_capacity(vehicle, destination_demand):
    """Return true if the vehicle has enough capacity to handle its next location

    Parameters:
    vehicle: The vehicle
    destination_demand: Destination demand
    """
    return vehicle.capacity_left >= destination_demand


def define_visit_order(vehicle, distances, times, visits):
    """Return a possible Visit array

    Parameters:
    vehicle: The vehicle
    visits: Visit list 
    """
    possible_visit_list = VisitLinkedList()
    possible_visit_list.add_last(visits[0])
    for current_visit, next_visit in zip(visits, visits[1:]):
        current_visit_id = current_visit.visit_id
        next_visit_id = next_visit.visit_id
        # Checking if energy level is enough
        if has_enough_energy(vehicle, distances, current_visit_id, next_visit_id):
            print("enough energy for visit {0} to {1}".format(
                current_visit_id, next_visit_id))
        else:
            print("we stop here, not enough energy for visit {0} to {1}".format(
                current_visit_id, next_visit_id))
            break
        # Checking if working time is enough
        if has_enough_time(vehicle, times, current_visit_id, next_visit_id):
            print("enough time for visit {0} to {1}".format(
                current_visit_id, next_visit_id))
        else:
            print("we stop here, not enough time for visit {0} to {1}".format(
                current_visit_id, next_visit_id))
            break
        # Checking if capacity is enough
        if has_enough_capacity(vehicle, next_visit.demand):
            print("enough capacity for visit {0} to {1}".format(
                current_visit_id, next_visit_id))
            possible_visit_list.add_last(next_visit)
            vehicle.consume_energy(get_distance(
                distances, current_visit_id, next_visit_id))
            vehicle.consume_time(datetime.timedelta(
                seconds=get_time(times, current_visit_id, next_visit_id)))
            vehicle.consume_capacity(next_visit.demand)
        else:
            print("we stop here, not enough capacity for visit {0} to {1}".format(
                current_visit_id, next_visit_id))
            break
    return possible_visit_list
