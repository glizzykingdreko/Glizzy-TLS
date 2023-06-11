# Glizzy TLS

![Banner](./image/logo.png)

Glizzy TLS is a Python module that brings the power and flexibility of Go's TLS implementation to Python. It's designed to offer TLS (Transport Layer Security) capabilities in Python while taking advantage of the performance benefits of Go.


## Table of Contents
- [Glizzy TLS](#glizzy-tls)
  - [Table of Contents](#table-of-contents)
  - [Disclaimer](#disclaimer)
  - [What is TLS?](#what-is-tls)
  - [Why Glizzy TLS?](#why-glizzy-tls)
  - [How is it done?](#how-is-it-done)
  - [Installation](#installation)
  - [Example Usage](#example-usage)
    - [Session Objects](#session-objects)
    - [Custom Client Hello](#custom-client-hello)
    - [Supported Parameters for `Session`](#supported-parameters-for-session)
    - [Supported Parameters for `request`](#supported-parameters-for-request)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact Me](#contact-me)
  

## Disclaimer
This is a first implementation of TLS in python for non supported platforms from other modules. I've quickly done it for a project I'm working on. I'll improve it by adding more features as soon as I can.

Check out the [source code on GitHub](https://github.com/glizzykingdreko/Glizzy-TLS)

## What is TLS?

Transport Layer Security (TLS) is a protocol that provides privacy and data integrity between two communicating applications. It's used for web browsers and other applications that require data to be securely exchanged over a network.

## Why Glizzy TLS?

While there are existing Python libraries for TLS, they can sometimes fall short in terms of performance and compatibility. Go has a robust and performant TLS library, and by compiling Go code to a shared object (`.so`) file and interfacing with it using CPython's `ctypes` library, Glizzy TLS brings this power to Python.

Moreover, the following key points make Glizzy TLS stand out:

- **Platform Independence**: Unlike other libraries that come with pre-compiled `.so` files, Glizzy TLS compiles the Go source code during installation. This means it can be used on any operating system without any modifications.
- **Open Source and Customizable**: The Go source code for the `.so` file is publicly available. This means you can make any edits or customizations that you need for your specific use case.
- **Shared Memory**: Glizzy TLS uses shared memory to communicate between Python and Go. This means that the data is not copied between the two languages, which can lead to significant performance improvements.
- **Shared cookies in Session Objects**: Session objects can be used to share cookies between requests. This is useful for applications that require authentication.

## How is it done?

The core of Glizzy TLS is the Go TLS implementation, which is compiled to a `.so` file during installation. This file is then loaded and interfaced with in Python using the `ctypes` library. This allows Python code to call the Go functions directly, offering a seamless integration between the two languages.

## Installation

You can install Glizzy TLS with pip:

```bash
pip install glizzy-tls
```

Please note that Glizzy TLS requires Go to be installed on your system. You can download it from [here](https://golang.org/dl/).

## Example Usage

Glizzy TLS is designed to be as simple as possible and follows the same structure as Python's `requests` library. Here's an example of a simple HTTPS request:

```python
import glizzy_tls

response = glizzy_tls.get("https://example.com")

print(response.status_code)
print(response.text)
```

### Session Objects
```python
from glizzy_tls import Session

# Create a TLS session
session = Session()
response = session.get("https://tls.peet.ws/api/all")
print(response.json()['tls']['ja3'])
```

### Custom Client Hello
```python
from glizzy_tls import Session

# Create a TLS session
session = Session(client_hello="chrome_112")
response = session.get("https://tls.peet.ws/api/all")

# Print the response
print(response.json()['tls']['ja3'])
```

See the [examples](examples) directory for more examples.

### Supported Parameters for `Session`
 - `client_hello`: The client hello to use. Defaults to `chrome_112`.

### Supported Parameters for `request`
 - `method`: The HTTP method to use. Defaults to `GET`.
 - `url`: The URL to request.
 - `headers`: A dictionary of headers to send with the request.
 - `body`: The body of the request.
 - `cookies`: A dictionary of cookies to send with the request.
 - `proxy`: The proxy to use. Defaults to `None`.
 - `follow_redirects`: Whether to follow redirects. Defaults to `True`.
 - `timeout_seconds`: The timeout in seconds. Defaults to `10`.
 - `details`: Whether to return detailed information about the request. Defaults to `False`. Will return a `RequestDetails` object instead of a `Response` object.


## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

Glizzy TLS is licensed under the [MIT License](LICENSE).

## Contact Me

If you have any questions, issues or just want to connect, feel free to reach out or follow me on these platforms:

- [GitHub](https://github.com/Glizzykingdreko)
- [Twitter](https://twitter.com/Glizzykingdreko)
- [Medium](https://medium.com/@Glizzykingdreko)
- [Mail](mailto:glizzykingdreko@protonmail.com)  