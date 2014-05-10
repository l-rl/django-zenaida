from django.db import models as db_models
from django.forms import models
from django.utils import six
from floppyforms.fields import (CharField, IntegerField, DateField, TimeField,
                                DateTimeField, EmailField, FileField,
                                ImageField, URLField, BooleanField,
                                NullBooleanField, FloatField, DecimalField,
                                SlugField, IPAddressField, FilePathField,
                                GenericIPAddressField, TypedChoiceField)
from floppyforms.forms import LayoutRenderer
from floppyforms.models import ModelChoiceField, ModelMultipleChoiceField
from floppyforms.widgets import *
from zenaida.widgets import SplitDateTimeWidget

FORMFIELD_OVERRIDES = {
    db_models.BooleanField: {'form_class': BooleanField},
    db_models.CharField: {'form_class': CharField},
    db_models.CommaSeparatedIntegerField: {'form_class': CharField},
    db_models.DateField: {'form_class': DateField},
    db_models.DateTimeField: {'form_class': DateTimeField, 'widget': SplitDateTimeWidget},
    db_models.DecimalField: {'form_class': DecimalField},
    db_models.EmailField: {'form_class': EmailField},
    db_models.FilePathField: {'form_class': FilePathField},
    db_models.FloatField: {'form_class': FloatField},
    db_models.IntegerField: {'form_class': IntegerField},
    db_models.BigIntegerField: {'form_class': IntegerField},
    db_models.IPAddressField: {'form_class': IPAddressField},
    db_models.GenericIPAddressField: {'form_class': GenericIPAddressField},
    db_models.NullBooleanField: {'form_class': NullBooleanField},
    db_models.PositiveIntegerField: {'form_class': IntegerField},
    db_models.PositiveSmallIntegerField: {'form_class': IntegerField},
    db_models.SlugField: {'form_class': SlugField},
    db_models.SmallIntegerField: {'form_class': IntegerField},
    db_models.TextField: {'form_class': CharField, 'widget': Textarea},
    db_models.TimeField: {'form_class': TimeField},
    db_models.URLField: {'form_class': URLField},
    db_models.BinaryField: {'form_class': CharField},

    db_models.FileField: {'form_class': FileField},
    db_models.ImageField: {'form_class': ImageField},

    db_models.ForeignKey: {'form_class': ModelChoiceField},
    db_models.ManyToManyField: {'form_class': ModelMultipleChoiceField},
    db_models.OneToOneField: {'form_class': ModelChoiceField},
}


for value in FORMFIELD_OVERRIDES.values():
    value['choices_form_class'] = TypedChoiceField


def formfield_callback(db_field, **kwargs):
    defaults = FORMFIELD_OVERRIDES.get(db_field.__class__, {}).copy()
    defaults.update(kwargs)
    return db_field.formfield(**defaults)


class ModelFormMetaclass(models.ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if not attrs.get('formfield_callback'):
            attrs['formfield_callback'] = formfield_callback
        return super(ModelFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


# Necessary because we use django.utils.six (v 1.5.2), which only
# allows a single parent class for with_metaclass.
class _ModelForm(LayoutRenderer, models.ModelForm):
    pass


class ModelForm(six.with_metaclass(ModelFormMetaclass, _ModelForm)):
    pass


def modelform_factory(model, form=ModelForm, *args, **kwargs):
    return models.modelform_factory(model, form, *args, **kwargs)


def modelformset_factory(model, form=ModelForm, *args, **kwargs):
    return models.modelformset_factory(model, form, *args, **kwargs)


def inlineformset_factory(parent_model, model, form=ModelForm,
                          *args, **kwargs):
    return models.inlineformset_factory(parent_model, model, form,
                                        *args, **kwargs)


### END FLOPPYFORMS PORT ###


class MemoModelForm(ModelForm):
    # Subclass of ModelForm that memoizes querysets. For use in
    # complex formsets.
    def __init__(self, memo_dict, *args, **kwargs):
        self.memo_dict = memo_dict
        super(MemoModelForm, self).__init__(*args, **kwargs)

    def _model_and_qs(self, model_or_qs):
        if isinstance(model_or_qs, db_models.query.QuerySet):
            qs = model_or_qs
            model = qs.model
        else:
            model = model_or_qs
            qs = model.objects.all()

        return model, qs

    def get(self, model_or_qs, **kwargs):
        model, qs = self._model_and_qs(model_or_qs)
        key = frozenset(['get', model] + [item for item in kwargs.items()])
        if key not in self.memo_dict:
            try:
                self.memo_dict[key] = qs.get(**kwargs)
            except model.DoesNotExist:
                self.memo_dict[key] = None

        if self.memo_dict[key] is None:
            raise model.DoesNotExist
        return self.memo_dict[key]

    def filter(self, model_or_qs, **kwargs):
        model, qs = self._model_and_qs(model_or_qs)
        key = frozenset(['filter', model] + [item for item in kwargs.items()])
        if key not in self.memo_dict:
            self.memo_dict[key] = qs.filter(**kwargs)
        return self.memo_dict[key]

    def set_choices(self, field_name, model_or_qs, **kwargs):
        qs = self.filter(model_or_qs, **kwargs)
        field = self.fields[field_name]
        field.queryset = qs
        field.cache_choices = True
        field.choice_cache = [
            (field.prepare_value(obj), field.label_from_instance(obj))
            for obj in qs
        ]
