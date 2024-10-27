import requests
from .circuitBreaker import CircuitBreaker

cb = CircuitBreaker()


def get_data_from_service(service_url, headers={}, timeout=5):
    if cb.try_connect(service_url):
        try:
            response = requests.get(service_url, timeout=timeout, headers=headers)
            cb.connection_successful(service_url)
            return response
        except:
            cb.connection_error(service_url)
            return None


def post_data_to_service(service_url, headers={}, timeout=5, data={}):
    if cb.try_connect(service_url):
        try:
            response = requests.post(service_url, timeout=timeout, headers=headers, json=data)
            cb.connection_successful(service_url)
            return response
        except:
            cb.connection_error(service_url)
            return None


def patch_data_to_service(service_url, headers={}, timeout=5, data={}):
    if cb.try_connect(service_url):
        try:
            response = requests.patch(service_url, timeout=timeout, headers=headers, json=data)
            cb.connection_successful(service_url)
            return response
        except:
            cb.connection_error(service_url)
            return None


def delete_data_from_service(service_url, headers={}, timeout=5):
    if cb.try_connect(service_url):
        try:
            response = requests.delete(service_url, timeout=timeout, headers=headers)
            cb.connection_successful(service_url)
            return response
        except:
            cb.connection_error(service_url)
            return None