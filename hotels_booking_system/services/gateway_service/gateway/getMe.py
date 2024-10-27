import os
import json

from quart import Blueprint, Response, request
from .serviceRequests import get_data_from_service

getmeb = Blueprint('get_me', __name__, )


@getmeb.route('/api/v1/me', methods=['GET'])
async def get_me() -> Response:
    if 'X-User-Name' not in request.headers.keys():
        return Response(status=400, content_type='application/json',
                        response=json.dumps({'message': 'User name missing'}))

    response = get_data_from_service(
        'http://' + os.environ['RESERVATION_SERVICE_HOST'] + ':' + os.environ['RESERVATION_SERVICE_PORT'] + '/api/v1/reservations',
        timeout=5, headers={'X-User-Name': request.headers['X-User-Name']})

    if response is None:
        return Response(status=503, content_type='application/json',
                        response=json.dumps({'message': 'Reservation Service unavailable'}))

    reservations = response.json()
    for res in reservations:
        response = get_data_from_service(
            'http://' + os.environ['RESERVATION_SERVICE_HOST'] + ':' + os.environ['RESERVATION_SERVICE_PORT'] + '/api/v1/hotels/' +
            res['hotel_id'], timeout=5)

        if response is None:
            return Response(status=503, content_type='application/json',
                            response=json.dumps({'message': 'Reservation Service unavailable'}))

        del res['hotel_id']
        res['hotel'] = response.json()

        response = get_data_from_service('http://' + os.environ['PAYMENT_SERVICE_HOST'] + ':' + os.environ[
            'PAYMENT_SERVICE_PORT'] + '/api/v1/payment/' + res['paymentUid'], timeout=5)

        del res['paymentUid']
        if response is None:
            res['payment'] = {}
        elif response.status_code != 200:
            return Response(status=response.status_code, content_type='application/json', response=response.text)
        else:
            res['payment'] = response.json()

    response = get_data_from_service('http://' + os.environ['LOYALTY_SERVICE_HOST'] + ':' + os.environ[
        'LOYALTY_SERVICE_PORT'] + '/api/v1/loyalty', timeout=5,
                                     headers={'X-User-Name': request.headers['X-User-Name']})
    if response is None:
        loyalty = {}
    elif response.status_code != 200:
        return Response(status=response.status_code, content_type='application/json', response=response.text)
    else:
        loyalty = response.json()

    result = {
        'reservations': reservations,
        'loyalty': loyalty
    }
    return Response(status=200, content_type='application/json', response=json.dumps(result))
