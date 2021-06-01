from django import forms

from habit.models import Habit


class HabitForm(forms.ModelForm):
    """
    Form for creating a new habit
    """

    class Meta:
        model = Habit
        exclude = ['user', 'closing']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'opening': forms.DateInput(attrs={'class': "form-control"}),
            'term': forms.NumberInput(attrs={'class': "form-control"}),
            'days_per_week': forms.CheckboxSelectMultiple(attrs={'class': "form-check-input"}),
        }

