import os
import json
import time
import asyncio
from urllib.parse import urlparse
from quart import Blueprint, Response, request
from .serviceRequests import send_request_to_service


postqueueb = Blueprint('post_queue', __name__, )


@postqueueb.route('/api/v1/post_queue', methods=['POST'])
async def post_queue() -> Response:
    data = await request.body
    request_data = json.loads(data)
    parsed_url = urlparse(request_data['url'])
    service_name = parsed_url.hostname
    cur_request = {'method': request_data['method'],
                   'url': request_data['url'],
                   'headers': request_data['headers'],
                   'body': {}}
    response = send_request_to_service(service_name, cur_request)
    while response is None:
        await asyncio.sleep(10)
        response = send_request_to_service(service_name, cur_request)
    return Response(
        status=200
    )
