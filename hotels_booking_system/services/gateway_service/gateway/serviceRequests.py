import requests
from .circuitBreaker import CircuitBreaker
from urllib.parse import urlparse

cb = CircuitBreaker()
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