from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from orders.models import Item, Extra


# custom form to workaround problem with bidirectional m2m in django admin
# https://code.djangoproject.com/ticket/897
# based on https://gist.github.com/Grokzen/a64321dd69339c42a184
class ExtraAdminForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Items'),
            is_stacked=False
        )
    )

    class Meta:
        model = Extra
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExtraAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['items'].initial = self.instance.items.all()

    def save(self, commit=True):
        extra = super(ExtraAdminForm, self).save(commit=False)

        if commit:
            extra.save()

        if extra.pk:
            extra.items.set(self.cleaned_data['items'])
            extra.save()

        return extra

# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
#
# from .models import Meal, Ingredient, MenuItemType
#
#
# class UserRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, help_text='first name')
#     last_name = forms.CharField(max_length=30, help_text='last name')
#     email = forms.EmailField(max_length=200, help_text='Your email.')
#
#     class Meta:
#         model = User
#         fields = (
#             'username', 'first_name', 'last_name', 'email', 'password1',
#             'password2')
#
#
# class UserLoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#
# class MealSelectForm(forms.ModelForm):
#     class Meta:
#         model = Meal
#         fields = ('type', 'meal', 'extras', 'toppings', 'special_instructions')
#
#     type = forms.ModelChoiceField(queryset=MenuItemType.objects.all())
#     meal = forms.ModelChoiceField(queryset=Meal.objects.all())
#
#     extras = forms.ModelMultipleChoiceField(
#         queryset=Ingredient.objects.all(), required=False)
#     toppings = forms.ModelMultipleChoiceField(
#         queryset=Ingredient.objects.all(), required=False)
#     special_instructions = forms.CharField(
#         max_length=300, help_text='Special instructions', required=False)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['meal'].widget.attrs = {'style': 'display:none;'}
#
#
#
