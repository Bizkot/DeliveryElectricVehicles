from django.http import HttpResponse
import csv
import io
import numpy

from django.views.decorators.csrf import csrf_exempt

from api.visit import Visit


def index(request):
    return HttpResponse("Hello world. You're at the api index.")


@csrf_exempt
def first_heuristic(request):
    if request.method == 'POST':
        if request.FILES:
            visits_file = request.FILES.get('visits')
            distance = request.FILES.get('distance')
            times = request.FILES.get('times')
            vehicle = request.FILES.get('vehicle')
            decoded_visits_file = visits_file.read().decode('latin-1')
            io_string = io.StringIO(decoded_visits_file)
            line_count = 0
            visits = []
            for visit in csv.reader(io_string, delimiter=',', quotechar='|'):
                if line_count == 0:
                    pass
                else:
                    visits.append(Visit(visit[0], visit[1], visit[2], visit[3], visit[4]))
                line_count += 1
            return HttpResponse("First heuristic is done")
        else:
            return HttpResponse("Files not found")
    else:
        return HttpResponse("Wrong method")
