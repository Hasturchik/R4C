import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from .forms import RobotForm
from .models import Robot


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            form = RobotForm(data)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                created_date = parse_datetime(str(cleaned_data['created']))
                robot_serial = f"{cleaned_data['model']}{cleaned_data['version']}"
                robot = Robot(
                    serial=robot_serial,
                    model=cleaned_data['model'],
                    version=cleaned_data['version'],
                    created=created_date
                )
                robot.save()

                return JsonResponse({"message": "Robot created successfully.", "robot_serial": robot_serial}, status=201)
            else:
                return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
