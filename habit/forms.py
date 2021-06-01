from django import forms

from habit.models import Habit


class HabitForm(forms.ModelForm):
    """
    Form for creating a new habit
    """

    class Meta:
        model = Habit
        exclude = ['user', 'closing']

