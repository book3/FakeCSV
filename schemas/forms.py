from django import forms
from django.core.exceptions import ValidationError

from .models import Column, Schema


class SchemaForm(forms.ModelForm):
    title = forms.CharField(
        label="Name", widget=forms.TextInput(attrs={"class": "form-control  mb-3"})
    )
    column_separator = forms.CharField(
        label="Column Separator",
        widget=forms.Select(
            attrs={"class": "form-control form-select mb-3"},
            choices=Schema.COLUMN_SEPARATORS,
        ),
    )
    string_character = forms.CharField(
        label="String Character",
        widget=forms.Select(
            attrs={"class": "form-control form-select mb-3"},
            choices=Schema.STRING_CHARACTERS,
        ),
    )

    class Meta:
        model = Schema
        fields = ("title", "column_separator", "string_character")


class ColumnForm(forms.ModelForm):
    name = forms.CharField(
        label="Column name", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    type = forms.CharField(
        label="Type",
        widget=forms.Select(
            attrs={"class": "form-control form-select int-range"},
            choices=Column.COLUMN_TYPES,
        ),
    )
    start_value = forms.IntegerField(
        label="From",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )
    end_value = forms.IntegerField(
        label="To",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )
    order = forms.IntegerField(
        label="Order",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        column_type = cleaned_data.get("type", None)
        if column_type == "Integer":
            start_value = cleaned_data.get("start_value", None)
            end_value = cleaned_data.get("end_value", None)

            if not start_value:
                self.add_error("start_value", "Provide start_value")
                raise ValidationError("Provide both start and end value")
            if not end_value:
                self.add_error("end_value", "Provide end_value")
                raise ValidationError("Provide both start and end value")
            if start_value and end_value:
                if start_value >= end_value:
                    self.add_error("start_value", "start must be less than end value")
                    raise ValidationError("Start value must be less than end value")
        return self.cleaned_data

    class Meta:
        model = Column
        fields = ("name", "type", "start_value", "end_value", "order")


ColumnFormSet = forms.inlineformset_factory(Schema, Column, form=ColumnForm, extra=1)
