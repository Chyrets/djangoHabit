from datetime import datetime, timedelta

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from habit.forms import HabitForm
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

        for x in range(len(habit.days_per_week)):
            print(habit.days_per_week[x])

        context = {
            'habit': habit,
            'days': days,
            'months': months,
            'progress': progress,
            'percent': percent
        }

        return render(request, 'habit/habit.html', context)

    def post(self, request, habit_pk, *args, **kwargs):
        habit = Habit.objects.get(id=habit_pk, user=request.user)

        if 'delete' in request.POST:
            habit.delete()

        return HttpResponseRedirect(reverse('main'))


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


class CreateHabitView(View):
    """

    """
    form_class = HabitForm
    template_name = 'habit/create_habit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        opening = datetime.strptime(request.POST.get('opening'), '%Y-%m-%d')
        term = int(request.POST.get('term'))
        Habit.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            user=request.user,
            opening=opening,
            term=term,
            closing=opening + timedelta(term),
            days_per_week=request.POST.getlist('days_per_week')
        )

        return redirect(reverse('main'))
