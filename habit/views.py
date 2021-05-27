from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from habit.models import Day, Habit


class MainPageView(View):
    """
    This page display tasks for today
    """

    def get(self, request, *args, **kwargs):
        habits = Habit.objects.filter(day__date=datetime.today(), user=request.user)

        context = {
            'habits': habits,
        }

        return render(request, 'habit/main.html', context)


class AllHabitView(View):
    """
    Display list of user habits
    """

    def get(self, request, *args, **kwargs):
        habits = Habit.objects.filter(user=request.user)

        return render(request, 'habit/main.html', {'habits': habits})


class HabitView(View):
    """
    Display complete information about the habit
    """

    def get(self, request, habit_pk, *args, **kwargs):
        habit = Habit.objects.get(id=habit_pk, user=request.user)
        days = Day.objects.filter(habit=habit)

        months = days.annotate(unique_month=TruncMonth('date')).values('unique_month').annotate(c=Count('id'))

        progress = datetime.today().date() - habit.opening
        percent = (progress.days / habit.term) * 100

        context = {
            'habit': habit,
            'days': days,
            'months': months,
            'progress': progress,
            'percent': percent
        }

        return render(request, 'habit/habit.html', context)


class DayView(View):
    """
    Display complete information about the day
    """

    def get(self, request, day_pk, *args, **kwargs):
        day = Day.objects.get(id=day_pk, habit__user=request.user)
        today = datetime.today().date()

        context = {
            'day': day,
            'today': today
        }

        return render(request, 'habit/day.html', context)

    def post(self, request, day_pk, *args, **kwargs):
        day = Day.objects.get(id=day_pk, habit__user=request.user)

        if 'save-status' in request.POST:
            day.status = request.POST.get('status')[2]
            day.save()
        elif 'save-note' in request.POST:
            day.note = request.POST.get('note')
            day.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
