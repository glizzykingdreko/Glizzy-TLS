package main

import (
	"C"
	"encoding/json"
	"fmt"
	fhttp "github.com/bogdanfinn/fhttp"
	tls_client "github.com/bogdanfinn/tls-client"
	"io/ioutil"
	"log"
	"net/url"
	"strings"
)

type cookieStruct struct {
	Name   string `json:"name"`
	Value  string `json:"value"`
	Domain string `json:"domain"`
}

type RequestDetails struct {
	Method      string            `json:"method"`
	URL         string            `json:"url"`
	Headers     map[string]string `json:"headers"`
	ClientHelloId string            `json:"client_hello"`
	Cookies     []*fhttp.Cookie    `json:"cookies"`
}

type ResponseDetails struct {
	StatusCode int               `json:"statusCode"`
	Body       string            `json:"body"`
	Headers    map[string]string `json:"headers"`
	Cookies    []*fhttp.Cookie   `json:"cookies"`
}

type FinalResponse struct {
	Request  RequestDetails  `json:"request"`
	Response ResponseDetails `json:"response"`
}

//export SendTlsRequest
func SendTlsRequest(method *C.char, urlStr *C.char, headers *C.char, body *C.char, cookies *C.char, proxy *C.char, followRedirects C.int, timeoutSeconds C.int, clientProfile *C.char) *C.char {
	gMethod := C.GoString(method)
	gUrl := C.GoString(urlStr)
	gHeaders := C.GoString(headers)
	gBody := C.GoString(body)
	gCookies := C.GoString(cookies)
	gProxy := C.GoString(proxy)
	gFollowRedirects := int(followRedirects) != 0
	gTimeoutSeconds := int(timeoutSeconds)
	gClientProfile := C.GoString(clientProfile)

	var headerMap map[string]string
	json.Unmarshal([]byte(gHeaders), &headerMap)

	jar := tls_client.NewCookieJar()
	var clientProfileValue tls_client.ClientProfile
	// you need to replace this switch statement with the correct mapping from string to tls_client.ClientProfile
	switch gClientProfile {
	case "Chrome_105":
		clientProfileValue = tls_client.Chrome_105
	case "Chrome_106":
		clientProfileValue = tls_client.Chrome_106
	case "Chrome_107":
		clientProfileValue = tls_client.Chrome_107
	case "Chrome_108":
		clientProfileValue = tls_client.Chrome_108
	case "Chrome_109":
		clientProfileValue = tls_client.Chrome_109
	case "Chrome_110":
		clientProfileValue = tls_client.Chrome_110
	case "Chrome_111":
		clientProfileValue = tls_client.Chrome_111
	case "Chrome_112":
		clientProfileValue = tls_client.Chrome_112
	default:
		clientProfileValue = tls_client.Chrome_112
	}

	options := []tls_client.HttpClientOption{
		tls_client.WithTimeoutSeconds(gTimeoutSeconds),
		tls_client.WithClientProfile(clientProfileValue),
		tls_client.WithCookieJar(jar),
	}

	client, err := tls_client.NewHttpClient(tls_client.NewNoopLogger(), options...)
	if err != nil {
		log.Println(err)
		return C.CString(fmt.Sprintf("{\"error\": \"%v\"}", err.Error()))
	}

	if gProxy != "" {
		err := client.SetProxy(gProxy)
		if err != nil {
			log.Println(err)
			return C.CString(fmt.Sprintf("{\"error\": \"%v\"}", err.Error()))
		}
	}

	if gFollowRedirects {
		client.SetFollowRedirect(true)
	} else {
		client.SetFollowRedirect(false)
	}

	req, err := fhttp.NewRequest(gMethod, gUrl, strings.NewReader(gBody))
	if err != nil {
		log.Println(err)
		return C.CString(fmt.Sprintf("{\"error\": \"%v\"}", err))
	}

	var headerOrder []string
	for key, value := range headerMap {
		req.Header[key] = []string{value}
		headerOrder = append(headerOrder, key)
	}
	req.Header[fhttp.HeaderOrderKey] = headerOrder


	cookieList := []*fhttp.Cookie{}
	if gCookies != "" {
		// Unmarshal gCookies into a slice of cookieStruct
		var cookies []cookieStruct
		json.Unmarshal([]byte(gCookies), &cookies)
	
		for _, cookieData := range cookies {
			cookie := &fhttp.Cookie{
				Name:   cookieData.Name,
				Value:  cookieData.Value,
				Domain: cookieData.Domain,
			}
			cookieList = append(cookieList, cookie)
	
			// Only set domain if specified
			if cookieData.Domain != "" {
				cookie.Domain = cookieData.Domain
				cookieURL, _ := url.Parse("https://" + cookieData.Domain)
				jar.SetCookies(cookieURL, []*fhttp.Cookie{cookie})
			}
		}
	}

	resp, err := client.Do(req)
	if err != nil {
		log.Println(err)
		return C.CString(fmt.Sprintf("{\"error\": \"%v\"}", err))
	}

	defer resp.Body.Close()

	statusCode := resp.StatusCode
	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Println(err)
		return C.CString(fmt.Sprintf("{\"error\": \"%v\"}", err))
	}

	responseHeaders := make(map[string]string)
	for key, values := range resp.Header {
		responseHeaders[key] = strings.Join(values, ", ")
	}

	requestDetails := RequestDetails{
		Method:  gMethod,
		URL:     gUrl,
		Headers: headerMap,
		ClientHelloId:  tls_client.Chrome_105.GetClientHelloStr(),
		Cookies: cookieList,
	}

	responseDetails := ResponseDetails{
		StatusCode: statusCode,
		Body:       string(bodyBytes),
		Headers:    responseHeaders,
		Cookies:    client.GetCookieJar().Cookies(req.URL),
	}

	finalResponse := FinalResponse{
		Request:  requestDetails,
		Response: responseDetails,
	}

	finalResponseJSON, err := json.Marshal(finalResponse)
	if err != nil {
		log.Println(err)
		return C.CString(fmt.Sprintf("{\"error\": \"%v\"}", err))
	}

	return C.CString(string(finalResponseJSON))
}

func main() {}