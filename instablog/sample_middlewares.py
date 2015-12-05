# sample_middlewares.py


class SampleMiddleware(object):
    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'
