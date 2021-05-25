from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.views import View

from habit.models import Day, Habit


class MainPageView(View):
    """
    This page display tasks for today
    """

    def get(self, request, *args, **kwargs):
        tasks = Habit.objects.filter(day__date=datetime.today(), user=request.user)

        context = {
            'tasks': tasks
        }

        return render(request, 'habit/main.html', context)


class HabitView(View):
    """
    Display complete information about the habit
    """

    def get(self, request, habit_pk, *args, **kwargs):
        habit = Habit.objects.get(id=habit_pk, user=request.user)
        days = Day.objects.filter(habit=habit)

        months = days.annotate(unique_month=TruncMonth('date')).values('unique_month').annotate(c=Count('id'))

        context = {
            'habit': habit,
            'days': days,
            'months': months
        }

        return render(request, 'habit/habit.html', context)
