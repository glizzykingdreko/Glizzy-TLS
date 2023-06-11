from glizzy_tls import Session

if __name__ == "__main__":
    # Create a TLS session
    session = Session()
    response = session.get("https://tls.peet.ws/api/all")

    # Print the response
    print(response.json()['tls']['ja3'])