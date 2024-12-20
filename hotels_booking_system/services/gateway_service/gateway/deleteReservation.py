import os
import json

from quart import Blueprint, Response, request
from .serviceRequests import delete_data_from_service, post_data_to_service, get_data_from_service

deletereservationb = Blueprint('delete_reservation', __name__, )


@deletereservationb.route('/api/v1/reservations/<string:reservationUid>', methods=['DELETE'])
async def delete_reservation(reservationUid: str) -> Response:
    if 'X-User-Name' not in request.headers.keys():
        return Response(status=400, content_type='application/json',
                        response=json.dumps({'message': 'User name missing'}))

    response = delete_data_from_service('http://' + os.environ['RESERVATION_SERVICE_HOST'] + ':'
                                        + os.environ['RESERVATION_SERVICE_PORT'] + '/api/v1/reservations/'
                                        + reservationUid, timeout=5)

    if response is None:
        return Response(status=503, content_type='application/json',
                        response=json.dumps({'message': 'Reservation Service unavailable'}))
    elif response.status_code != 200:
        return Response(status=response.status_code, content_type='application/json', response=response.text)

    reservation = response.json()

    response = delete_data_from_service('http://' + os.environ['PAYMENT_SERVICE_HOST'] + ':'
                                        + os.environ['PAYMENT_SERVICE_PORT'] + '/api/v1/payment/'
                                        + reservation['paymentUid'], timeout=5)

    if response is None:
        return Response(status=503, content_type='application/json',
                        response=json.dumps({'message': 'Payment service unavailable'}))

    elif response.status_code != 200:
        return Response(status=response.status_code, content_type='application/json', response=response.text)

    response = delete_data_from_service(
        'http://' + os.environ['LOYALTY_SERVICE_HOST'] + ':' + os.environ['LOYALTY_SERVICE_PORT'] + '/api/v1/loyalty',
        timeout=5, headers={'X-User-Name': request.headers['X-User-Name']})

    if response is None:
        response = post_data_to_service(
            'http://' + os.environ['QUEUE_SERVICE_HOST'] + ':' + os.environ['QUEUE_SERVICE_PORT']
            + '/api/v1/post_queue', timeout=10,
            data={
                'method': 'DELETE',
                'url': (
                        'http://' + os.environ['LOYALTY_SERVICE_HOST'] + ':'
                        + os.environ['LOYALTY_SERVICE_PORT'] + '/api/v1/loyalty'
                ),
                'headers': {'X-User-Name': request.headers['X-User-Name']}
            })

    elif response.status_code != 200:
        return Response(status=response.status_code, content_type='application/json', response=response.text)

    return Response(status=204)
