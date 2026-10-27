from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import User


def home(request):
    # 1. Общее количество сотрудников (К3)
    total_employees = User.objects.count()

    # 2. 4 последних по дате приёма (К4)
    # Оптимизация: prefetch_related для навыков и изображений (К7)
    latest_employees = (
        User.objects.exclude(hire_date__isnull=True)  # Только те, у кого есть дата
        .order_by("-hire_date")[:4]
        .prefetch_related("employeeskill_set__skill", "images")
        .select_related("workplace")  # Если понадобится номер стола
    )

    context = {
        "total_employees": total_employees,
        "employees": latest_employees,
    }
    return render(request, "home.html", context)


def employee_list(request):
    # Оптимизация для списка (К7)
    employees_list = (
        User.objects.all()
        .order_by("-id")  # <-- Добавили сортировку
        .prefetch_related("employeeskill_set__skill", "images")
        .select_related("workplace")
    )

    # Пагинация по 10 (К5)
    paginator = Paginator(employees_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "employees/employee_list.html", {"page_obj": page_obj})


@login_required
def employee_detail(request, pk):
    # Оптимизация для детальной страницы (К7)
    employee = get_object_or_404(
        User.objects.prefetch_related(
            "employeeskill_set__skill", "images"
        ).select_related("workplace"),
        pk=pk,
    )
    return render(request, "employees/employee_detail.html", {"employee": employee})
