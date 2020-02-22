from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from orders.models import Item, Extra, Basket, Type


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


class AddToBasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ('type', 'item', 'extras_selected', 'special_info')

    type = forms.ModelChoiceField(queryset=Type.objects.all())
    extras_selected = forms.ModelMultipleChoiceField(
            queryset=Extra.objects.all(), required=False)

    special_info = forms.CharField(required=False)

