from floppyforms import widgets
from django.template import loader

class DateTimeLocalInput(widgets.DateTimeInput):
    input_type = "datetime-local"


class SplitDateTimeWidget(widgets.SplitDateTimeWidget):
    "SplitDateTimeWidget with a custom template."

    template_name = "floppyforms/splitdatetime.html"

    def format_output(self, rendered_widgets):
        context = {
            'widgets': rendered_widgets
        }
        return loader.render_to_string(
            self.template_name,
            dictionary=context)