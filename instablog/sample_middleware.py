class SampleMiddleware(object):
    def porcess_request(self, requset):
        request.just_say = 'Lorem Ipsum'
