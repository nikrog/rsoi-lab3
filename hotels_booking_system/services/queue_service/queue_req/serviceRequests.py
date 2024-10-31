import requests
from .circuitBreaker import CircuitBreaker
from .requestsQueue import RequestsQueue
from urllib.parse import urlparse

cb = CircuitBreaker()
rq = RequestsQueue()
GET_REQUEST_MAX_ATTEMPTS = 5


def get_data_from_service(service_url, headers={}, timeout=5):
    parsed_url = urlparse(service_url)
    service_name = parsed_url.hostname
    i = 0
    while i < GET_REQUEST_MAX_ATTEMPTS:
        if cb.try_connect(service_name):
            try:
                response = requests.get(service_url, timeout=timeout, headers=headers)
                cb.connection_successful(service_name)
                return response
            except:
                cb.connection_error(service_name)
        i += 1
    return None


def post_data_to_service(service_url, headers={}, timeout=5, data={}):
    parsed_url = urlparse(service_url)
    service_name = parsed_url.hostname
    if cb.try_connect(service_name):
        try:
            response = requests.post(service_url, timeout=timeout, headers=headers, json=data)
            cb.connection_successful(service_name)
            return response
        except:
            cb.connection_error(service_name)
            return None


def patch_data_to_service(service_url, headers={}, timeout=5, data={}):
    parsed_url = urlparse(service_url)
    service_name = parsed_url.hostname
    if cb.try_connect(service_name):
        try:
            response = requests.patch(service_url, timeout=timeout, headers=headers, json=data)
            cb.connection_successful(service_name)
            return response
        except:
            cb.connection_error(service_name)
            return None


def delete_data_from_service(service_url, headers={}, timeout=5):
    parsed_url = urlparse(service_url)
    service_name = parsed_url.hostname
    if cb.try_connect(service_name):
        try:
            response = requests.delete(service_url, timeout=timeout, headers=headers)
            cb.connection_successful(service_name)
            return response
        except:
            cb.connection_error(service_name)
            return None


def send_request_to_service(service_name, request):
    rq.push_request(service_name, request)
    empty_flag = False
    while empty_flag is False:
        cur_req = rq.pop_request()
        if cur_req is None:
            empty_flag = True
        else:
            cur_serv = list(cur_req.keys())[0]
            cur_req_data = list(cur_req.values())[0]
            method = cur_req_data['method']
            url = cur_req_data['url']
            headers = cur_req_data['headers']
            body = cur_req_data['body']
            response = None
            if method == 'POST':
                response = post_data_to_service(url, headers, body)
            elif method == 'GET':
                response = get_data_from_service(url, headers)
            elif method == 'PATCH':
                response = patch_data_to_service(url, headers, body)
            elif method == 'DELETE':
                response = delete_data_from_service(url, headers)
            if cur_serv == service_name and cur_req_data == request and response is not None:
                return response
            else:
                rq.push_request(cur_serv, cur_req_data)

