from json import dumps, loads
from typing import Union
import ctypes, os

from .exceptions import ExceptionSendingRequest, MissingGlizzyTlsLibrary
from .models import RequestDetails, Response
from .dependencies import build

# Load the shared library
build()
diectory = os.path.dirname(os.path.abspath(__file__))
try: lib = ctypes.cdll.LoadLibrary(f"{diectory}/libraries/libtls_client.so")
except OSError: raise MissingGlizzyTlsLibrary("Could not load the shared library")

# Specify the argument types for the SendTlsRequest function
lib.SendTlsRequest.argtypes = [
    ctypes.c_char_p,  # method
    ctypes.c_char_p,  # url
    ctypes.c_char_p,  # headers
    ctypes.c_char_p,  # body
    ctypes.c_char_p,  # cookies
    ctypes.c_char_p,  # proxy
    ctypes.c_int,     # follow_redirects
    ctypes.c_int,     # timeout_seconds
    ctypes.c_char_p   # client_hello
]

# Specify the return type for the GetAllClientProfiles function
lib.GetAllClientProfiles.restype = ctypes.c_char_p

# Specify the return type for the SendTlsRequest function
lib.SendTlsRequest.restype = ctypes.c_char_p

class Session:
    @staticmethod
    def get_all_client_profiles():
        """
        Get all client profiles from the Go shared library.

        Returns:
            list: A list of all client profiles.
        """
        try:
            # Call the GetAllClientProfiles function from the Go shared library
            profiles_json = lib.GetAllClientProfiles().decode('utf-8')
            # Convert the JSON string to a Python dictionary
            profiles_dict = loads(profiles_json)
            # Convert the dictionary to a list
            return list(profiles_dict.keys())
        except Exception as e:
            raise ExceptionSendingRequest(f"Failed to get client profiles: {e}")

    def __init__(self, client_hello: str="chrome_120"):
        """ 
        Create a new TLS session.

        Args:
            client_hello (str, optional): The client hello to use for this session. Defaults to "chrome_120".
        """
        self.client_hello = client_hello.encode('utf-8')
        self.cookies = []
    

    def request(self, method, url, headers: dict=None, data=None, cookies: list=None, proxy: str=None, follow_redirects: int=1, timeout_seconds: int=30, details: bool=False) -> Union[Response, RequestDetails]:
        """
        Send a TLS request using this session.

        Args:
            method (str): The HTTP method to use for this request.
            url (str): The URL to send the request to.
            headers (dict, optional): The headers to send with this request. Defaults to None.
            data (dict, optional): The body to send with this request. Defaults to None.
            cookies (list, optional): The cookies to send with this request. Defaults to None.
            proxy (str, optional): The proxy to use for this request. Defaults to None.
            follow_redirects (int, optional): Whether or not to follow redirects. Defaults to 1.
            timeout_seconds (int, optional): The number of seconds to wait for a response before timing out. Defaults to 30.
            details (bool, optional): Whether or not to return the request details. Defaults to False.
        """
        # Convert the parameters to JSON strings
        headers_json = dumps(headers).encode('utf-8') if headers else "".encode('utf-8')
        body_json = dumps(data).encode('utf-8') if data else "".encode('utf-8')

        # If no cookies were provided for this request, use the session cookies
        if not cookies:
            cookies = self.cookies

        # Process cookies
        cookies_list = []
        for cookie in cookies:
            cookie_dict = {
                "name": cookie["name"],
                "value": cookie["value"]
            }
            if "domain" in cookie:
                cookie_dict["domain"] = cookie["domain"]
            cookies_list.append(cookie_dict)

        cookies_json = dumps(cookies_list).encode('utf-8') if cookies_list else "".encode('utf-8')
        proxy_str = proxy.encode('utf-8') if proxy else "".encode('utf-8')

        # Call the SendTlsRequest function
        try:
            response_json = lib.SendTlsRequest(
                method.encode('utf-8'),
                url.encode('utf-8'),
                headers_json,
                body_json,
                cookies_json,
                proxy_str,
                follow_redirects,
                timeout_seconds,
                self.client_hello,
            ).decode()
        except Exception as e:
            raise ExceptionSendingRequest(e)

        # Convert the returned JSON string back to a Python dict
        request_details = RequestDetails(response_json)

        if cookies := request_details.response.cookies:
            # Handle cookies replaced by the server
            for cookie in cookies:
                cookie_dict = {
                    "name": cookie["Name"],
                    "value": cookie["Value"]
                }
                if "domain" in cookie:
                    cookie_dict["domain"] = cookie["Domain"]
                self.cookies.append(cookie_dict)

        return request_details.response if not details else request_details

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def head(self, url, **kwargs):
        return self.request('HEAD', url, **kwargs)
    
    def options(self, url, **kwargs):
        return self.request('OPTIONS', url, **kwargs)