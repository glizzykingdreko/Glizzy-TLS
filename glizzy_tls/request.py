from .session import Session

def request(method: str, url: str, *args, **kwargs):
    """
    Send a TLS request. Without a session.

    Args:
        method (str): The HTTP method to use for this request.
        url (str): The URL to send the request to.
        *args: The arguments to pass to the Session.request() method.
        **kwargs: The keyword arguments to pass to the Session.request() method.
    """
    client_hello = kwargs.pop('client_hello', 'Chrome_112')
    session = Session(client_hello)
    return session.request(method, url, *args, **kwargs)

def get(url: str, *args, **kwargs):
    """
    Send a TLS GET request. Without a session.

    Args:
        url (str): _description_
    """
    return request('GET', url, *args, **kwargs)

def post(url: str, *args, **kwargs):
    """
    Send a TLS POST request. Without a session.

    Args:
        url (str): _description_
    """
    return request('POST', url, *args, **kwargs)

def put(url: str, *args, **kwargs):
    """
    Send a TLS PUT request. Without a session.

    Args:
        url (str): _description_
    """
    return request('PUT', url, *args, **kwargs)