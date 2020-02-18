from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Meal


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='first name')
    last_name = forms.CharField(max_length=30, help_text='last name')
    email = forms.EmailField(max_length=200, help_text='Your email.')

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2')


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class MealSelectForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('type', 'meal')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meal'].widget.attrs = {'style': 'display:none;'}

    meal = forms.ModelChoiceField(queryset = Meal.objects.none())


