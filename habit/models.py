from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField


class Day(models.Model):
    """
    One day out of habit.
    Note - a word or two about this day.
    Date - date of the given day.
    Status - the status of the day.
    """
    SOON = '0'
    STATUS = (
        (SOON, 'Soon'),
        ('1', 'Completed'),
        ('2', 'Failed'),
        ('3', 'Another')
    )

    note = models.TextField(max_length=2550, null=True, blank=True)
    habit = models.ForeignKey('Habit', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS, default=SOON)


class Habit(models.Model):
    """
    Habit model.
    Title and description - a few words about habit.
    days_per_week - days to do habit
    user - habit author
    opening, closing - start and end dates
    term - numbers of days between opening and closing
    """
    ALL = '0'
    MON = '1'
    TUE = '2'
    WED = '3'
    THU = '4'
    FRI = '5'
    SAT = '6'
    SUN = '7'
    DAYS_PER_WEEK = [
        (ALL, 'All'),
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
        (SAT, 'Saturday'),
        (SUN, 'Sunday'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2550)
    days_per_week = MultiSelectField(choices=DAYS_PER_WEEK)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opening = models.DateField(default=datetime.today)
    term = models.IntegerField(default=71)
    closing = models.DateField(null=True, blank=True)

    def clean(self):
        if not self.closing:
            self.closing = self.opening + timedelta(self.term)

    def save(self, **kwargs):
        self.clean()
        return super().save(**kwargs)
