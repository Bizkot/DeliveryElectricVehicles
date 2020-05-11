from django.http import HttpResponse
import csv
import io
import numpy
import configparser

from django.views.decorators.csrf import csrf_exempt

from api.visit import Visit


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
            vehicle_config = load_vehicle_config(vehicle_config_file) 
            return HttpResponse("First heuristic is done")
        else:
            return HttpResponse("Files not found")
    else:
        return HttpResponse("Wrong method")


def load_visits(visits_file):
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
    distances = numpy.loadtxt(distance_file)
    return distances


def load_times(time_file):
    times = numpy.loadtxt(time_file)
    return times

# Not working at the moment ? (ask teacher)
def load_vehicle_config(vehicle_config_file):
    vehicle_config = configparser.ConfigParser()
    vehicle_config.read(vehicle_config_file)
    print(vehicle_config.sections())