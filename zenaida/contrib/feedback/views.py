import json

from django.http import (HttpResponse, HttpResponseNotAllowed,
                         HttpResponseBadRequest)

from zenaida.contrib.feedback.forms import FeedbackForm

def feedback_ajax_submit(request):
    if not request.POST:
        return HttpResponseNotAllowed(['POST'])
    else:
        form = FeedbackForm(request, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({}), content_type="application/json")
        else:
            return HttpResponseBadRequest(form.errors.as_json(), content_type="application/json")
