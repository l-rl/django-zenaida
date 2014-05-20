from django.db.models.query import QuerySet
import floppyforms.__future__ as forms


class MemoModelForm(forms.ModelForm):
    # Subclass of ModelForm that memoizes querysets. For use in
    # complex formsets.
    def __init__(self, memo_dict, *args, **kwargs):
        self.memo_dict = memo_dict
        super(MemoModelForm, self).__init__(*args, **kwargs)

    def _model_and_qs(self, model_or_qs):
        if isinstance(model_or_qs, QuerySet):
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
