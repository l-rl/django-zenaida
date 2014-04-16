import floppyforms as forms


CHOICES = (
    ('1', 'Choice 1'),
    ('2', 'Choice 2'),
    ('3', 'Choice 3'),
)


class Form1(forms.Form):
    char_field = forms.CharField()
    boolean_field = forms.BooleanField()
    choice_field = forms.ChoiceField(choices=CHOICES)
    radio_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    multi_select = forms.MultipleChoiceField(choices=CHOICES)
    checkbox_multiple_select = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)
