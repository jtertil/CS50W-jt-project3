from django import forms
from .models import Meal


class MealSelectForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('type', 'meal')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    meal = forms.ModelChoiceField(queryset = Meal.objects.none())



