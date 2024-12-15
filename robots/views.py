import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from .excel_report import create_excel_report
from .forms import RobotForm
from django.http import HttpResponse
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

@csrf_exempt
def get_excel_report(request):

    wb = create_excel_report()

    if wb is None:
        return HttpResponse("Nothing produced in the last week", content_type="text/plain")
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'

    wb.save(response)

    return response
