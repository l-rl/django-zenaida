from django.conf.urls import patterns, url
from django.views.generic import FormView

from test_project.example_app.forms import Form1


urlpatterns = patterns('',
    url(r'^',
        FormView.as_view(
            template_name="example_app/form1.html",
            form_class=Form1,
        ),
        name="form1"),
)
