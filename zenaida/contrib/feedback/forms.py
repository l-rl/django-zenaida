from django import forms
from django.contrib.auth import get_user_model
from django.core import serializers
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.translation import ugettext as _

from feedback.models import FeedbackItem

class FeedbackForm(forms.ModelForm):
    """
    A feedback form that creates a FeedbackItem object.

    The security implementation on this form is loosely based off of the
    implementation in django-contrib-comments.forms.CommentSecurityForm.

    """

    # Comprehensively, fields from the model:
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(),
                                  widget=forms.HiddenInput, required=True)
    view = forms.CharField(widget=forms.HiddenInput, required=True)
    content = forms.CharField(label=_("Your Message"), widget=forms.Textarea,
                              required=True)
    screenshot = forms.ImageField(label=_("Screenshot"), widget=forms.FileInput,
                                  required=False,
                                  help_text=_('Upload an optional screenshot, if applicable. <a href="http://www.take-a-screenshot.org/" target="_blank">How do I take a screenshot?</a>'))
    request_path = forms.CharField(widget=forms.HiddenInput, required=True)
    request_method = forms.CharField(widget=forms.HiddenInput, required=True)
    request_encoding = forms.CharField(widget=forms.HiddenInput, required=False)
    request_meta = forms.CharField(widget=forms.HiddenInput, required=False)
    request_get = forms.CharField(widget=forms.HiddenInput, required=False)
    request_post = forms.CharField(widget=forms.HiddenInput, required=False)
    request_files = forms.CharField(widget=forms.HiddenInput, required=False)
    # Field that handles tamper-proofing
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)

    def __init__(self, request=None, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)

        security_hash_dict = {
            'user': request.user if request.user.is_authenticated() else None,
            'view': request.resolver_match.view_name if request.resolver_match is not None else '',
            'request_path': request.path,
            'request_method': request.method,
            'request_encoding': request.encoding,
            'request_meta': dict(request.META),
            'request_get': dict(request.GET),
            'request_post': dict(request.POST),
            'request_files': dict(request.FILES),
        }
        security_hash = self.generate_security_hash(**security_hash_dict)

        self.initial.update(security_hash_dict)
        self.initial.update({'security_hash': security_hash})

    def clean_security_hash(self):
        """Check the security hash."""
        security_hash_dict = {
            'user': self.cleaned_data["user"],
            'view': self.cleaned_data["view"],
            'request_path': self.cleaned_data["request_path"],
            'request_method': self.cleaned_data["request_method"],
            'request_encoding': self.cleaned_data["request_encoding"],
            'request_meta': self.cleaned_data["request_meta"],
            'request_get': self.cleaned_data["request_get"],
            'request_post': self.cleaned_data["request_post"],
            'request_files': self.cleaned_data["request_files"],
        }
        expected_hash = self.generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if not constant_time_compare(expected_hash, actual_hash):
            raise forms.ValidationError("Form data has been tampered with.")
        return actual_hash

    def generate_security_hash(self, user, view, request_path, request_method,
                               request_encoding, request_meta, request_get,
                               request_post, request_files):
        """
        Generate a HMAC security hash from the provided info.
        """
        # Convert values to strings in order to hash them together:
        info = [str(x) if x is not None else "" for x in (user, view,
                request_path, request_method,
                request_encoding, request_meta, request_get,
                request_post, request_files)]
        key_salt = "feedback.FeedbackForm"
        value = "-".join(info)
        return salted_hmac(key_salt, value).hexdigest()

    class Meta:
        fields = (
            'user',
            'content',
            'screenshot',
            'view',
            'request_path',
            'request_method',
            'request_encoding',
            'request_meta',
            'request_get',
            'request_post',
            'request_files',
        )
        model = FeedbackItem
