from django.http import HttpResponse
import csv
import io
import numpy
import configparser

from django.views.decorators.csrf import csrf_exempt

from api.visit import Visit
from api.vehicle import Vehicle


def index(request):
    return HttpResponse("Hello world. You're at the api index.")


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
            return HttpResponse("First heuristic is done")
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
            visits.append(Visit(visit[0], visit[1],
                                visit[2], visit[3], visit[4]))
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
    vehicle = Vehicle(150, 100, 60, 180, 480, '07:00', '19:00')
    return vehicle

def get_distance(distances, origin, destination):
    """Return the distance between two locations

    Parameters:
    distances: Distance matrix
    origin: origin id
    destination: destination id
    """
    return distances.item((origin, destination))

def get_time(times, origin, destination):
    """Return the time between two locations

    Parameters:
    times: Time matrix
    origin: origin id
    destination: destination id
    """
    return times.item((origin, destination))