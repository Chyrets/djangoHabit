from datetime import datetime

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

        context = {
            'habit': habit,
            'days': days
        }

        return render(request, 'habit/habit.html', context)
