from django.forms.formsets import BaseFormSet


def make_form_or_formset_fields_not_required(form_or_formset):
    """Take a Form or FormSet and set all fields to not required."""
    if isinstance(form_or_formset, BaseFormSet):
        for single_form in form_or_formset:
            make_form_fields_not_required(single_form)
    else:
        make_form_fields_not_required(form_or_formset)


def make_form_fields_not_required(form):
    """Take a Form and set all fields to not required."""
    for field in form.fields.values():
        field.required = False
