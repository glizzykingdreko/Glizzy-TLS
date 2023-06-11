from glizzy_tls import get

if __name__ == "__main__":
    cookies = [
        {
            "name": "name",
            "value": "value"
        },
        {
            "name": "name2",
            "value": "value2",
            "domain": "example.com"
        }
    ]
    response = get("https://tls.peet.ws/api/all", cookies=cookies, client_hello="chrome_109")
    print(response.json()['tls']['ja3'])