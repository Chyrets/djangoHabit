from datetime import timedelta, datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from habit.models import Habit, Day


@receiver(post_save, sender=Habit)
def create_days_for_habit(sender, instance, created, **kwargs):
    if created:
        if instance.days_per_week == [instance.ALL]:
            for day in range(instance.term):
                Day.objects.create(
                    habit=instance,
                    date=instance.opening + timedelta(day)
                )
        else:
            date = instance.opening
            for day in range(instance.term):
                for week in instance.days_per_week:
                    if datetime.isoweekday(date) == int(week):
                        Day.objects.create(
                            habit=instance,
                            date=instance.opening + timedelta(day)
                        )
                date += timedelta(1)
