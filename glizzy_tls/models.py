from json import loads

from .exceptions import ExceptionReadingResponse, \
    ExceptionReceivingResponse

class Response:
    def __init__(self, response):
        # Set the response attributes
        self.status_code = response['statusCode']
        self.headers = response['headers']
        self.text = self.body = response['body']
        self.cookies = response['cookies']
    
    def json(self):
        return loads(self.body)

    def __str__(self):
        return f"Response(status_code={self.status_code})"

    def __repr__(self):
        return self.__str__()

class Request:
    def __init__(self, response):
        # Set the response attributes
        self.method = response['method']
        self.url = response['url']
        self.headers = response['headers']
        self.client_profile = self.client_hello = response['client_hello']
        self.cookies = response['cookies']

    def __str__(self):
        return f"RequestDetails(method={self.method}, url={self.url}, client_hellp={self.client_profile})"

    def __repr__(self):
        return self.__str__()

class RequestDetails:
    def __init__(self, response_json):
        # Convert the returned JSON string back to a Python dict
        try: response = loads(response_json)
        except: raise ExceptionReadingResponse(response_json)
        if 'error' in list(response):
            raise ExceptionReceivingResponse(response['error'])
        self.request = Request(response['request'])
        self.response = Response(response['response'])

    def __str__(self):
        return f"RequestDetails()"

    def __repr__(self):
        return self.__str__()
