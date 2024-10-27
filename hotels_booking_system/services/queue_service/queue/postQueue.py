import os
import json
import time

from quart import Blueprint, Response, request
from .serviceRequests import delete_data_from_service


rollbackrequestb = Blueprint('rollback_request', __name__, )


@rollbackrequestb.route('/api/v1/rollback_request', methods=['POST'])
async def rollback_request() -> Response:
    data = await request.body
    request_data = json.loads(data)
    response = delete_data_from_service(request_data['url'], request_data['headers'], timeout=10)
    while response is None:
        time.sleep(10)
        response = delete_data_from_service(
            request_data['url'], request_data['headers'], timeout=10)
    return Response(
        status=200
    )
