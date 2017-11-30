from django import forms

from viewflow_extensions.utils import make_form_or_formset_fields_not_required


class ExampleForm(forms.Form):
    text = forms.CharField()


ExampleFormSet = forms.formset_factory(ExampleForm)


def test_make_form_fields_not_required():
    f = ExampleForm({'text': ''})
    assert not f.is_valid()
    assert f.errors['text'] == ['This field is required.']

    f = ExampleForm({'text': ''})
    make_form_or_formset_fields_not_required(f)
    assert f.is_valid()


def test_make_formset_fields_not_required():
    data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '2',
        'form-MAX_NUM_FORMS': '',
        'form-0-text': 'text',
        'form-1-text': '',
    }
    fs = ExampleFormSet(data)
    assert not fs.is_valid()
    assert fs.errors[1]['text'] == ['This field is required.']

    fs = ExampleFormSet(data)
    make_form_or_formset_fields_not_required(fs)
    assert fs.is_valid()
