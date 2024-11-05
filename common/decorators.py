from functools import wraps

from django.http import HttpResponseBadRequest


def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return HttpResponseBadRequest(
                "Bad request: this endpoint only accepts AJAX requests."
            )
        return f(request, *args, **kwargs)

    return wrap
