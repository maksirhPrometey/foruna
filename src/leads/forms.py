from django import forms

from .models import Lead

_SOURCE_CHOICES = [('', '')] + Lead.SOURCE_CHOICES


class LeadForm(forms.Form):
    name = forms.CharField(
        label='Ім\'я',
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'lead-form__input',
            'placeholder': 'Ваше ім\'я',
            'autocomplete': 'name',
        }),
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'lead-form__input',
            'placeholder': '+38 0xx xxx xx xx',
            'inputmode': 'tel',
            'autocomplete': 'tel',
        }),
    )
    message = forms.CharField(
        label='Повідомлення',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'lead-form__input lead-form__textarea',
            'placeholder': 'Опишіть ваш запит (необов\'язково)',
            'rows': 3,
        }),
    )
    source = forms.ChoiceField(
        choices=_SOURCE_CHOICES,
        widget=forms.HiddenInput(),
        required=False,
    )
