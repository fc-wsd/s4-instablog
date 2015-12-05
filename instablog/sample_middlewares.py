# sample_middlewares.py

from django.shortcuts import render

from instablog.sample_exceptions import HelloWorldError


class SampleMiddleware(object):
    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'

    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            return render(request, 'error.html', {
                'error': exc,
                'status': 500,
            })
