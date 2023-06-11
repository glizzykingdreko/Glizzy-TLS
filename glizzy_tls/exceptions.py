
class TlsException(Exception):
    pass

class ExceptionSendingRequest(TlsException):
    pass

class ExceptionReadingResponse(TlsException):
    pass

class ExceptionReceivingResponse(TlsException):
    pass

class MissingGlizzyTlsLibrary(TlsException):
    pass