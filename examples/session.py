from glizzy_tls import Session

if __name__ == "__main__":
    # Create a TLS session
    print(Session.get_all_client_profiles())
    
    session = Session("chrome_120")
    response = session.get("https://tls.peet.ws/api/all")

    # Print the response
    print(response.json()['tls']['ja3'])