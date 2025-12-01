from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task
from .scoring import calculate_task_score
from datetime import datetime

@csrf_exempt
def analyze_tasks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        strategy = data.get("strategy")
        tasks = data.get("tasks")

        if tasks is None:
            return JsonResponse({"error": "Tasks missing in request"}, status=400)

        response_list = []

        for t in tasks:
            task_obj = Task.objects.create(
                title=t["title"],
                due_date=datetime.strptime(t["due_date"], "%Y-%m-%d").date(),
                importance=t["importance"],
                estimated_hours=t["estimated_hours"],
                dependencies=t.get("dependencies", [])
            )

            t["score"] = calculate_task_score(t)
            t["id"] = task_obj.id
            response_list.append(t)

        # Sorting logic based on strategy
        if strategy == "fastest":
            tasks_sorted = sorted(response_list, key=lambda x: x["estimated_hours"])
        elif strategy == "deadline":
            tasks_sorted = sorted(response_list, key=lambda x: x["due_date"])
        else:
            tasks_sorted = sorted(response_list, key=lambda x: x["score"], reverse=True)

        return JsonResponse(tasks_sorted, safe=False)

    return JsonResponse({"error": "POST only"}, status=400)

from datetime import date
@csrf_exempt
def suggest_tasks(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=400)

    today = date.today()

    # Fetch tasks for today
    tasks_today = Task.objects.filter(due_date=today)

    # If no tasks for today -> fallback to next available future date
    if not tasks_today.exists():
        next_task = Task.objects.filter(due_date__gt=today).order_by("due_date").first()
        
        if next_task:
            # Fetch all tasks for that next available future date
            tasks_today = Task.objects.filter(due_date=next_task.due_date)
        else:
            # No future tasks at all
            return JsonResponse({
                "top_3": [],
                "explanation": "No tasks available for today or future."
            })

    # Build list with dynamic scoring
    tasks_list = []
    for t in tasks_today:
        task_data = {
            "title": t.title,
            "due_date": t.due_date.strftime("%Y-%m-%d"),
            "importance": t.importance,
            "estimated_hours": t.estimated_hours,
            "dependencies": t.dependencies
        }
        # Dynamic score
        task_data["score"] = calculate_task_score(task_data)
        
        tasks_list.append(task_data)

    # Pick top 3
    top_three = sorted(tasks_list, key=lambda x: x["score"], reverse=True)[:3]

    return JsonResponse({
        "top_3": top_three,
        "explanation": "Top tasks based on urgency, importance, and effort."
    })
