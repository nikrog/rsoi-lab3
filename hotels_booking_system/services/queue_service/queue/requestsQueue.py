class RequestsQueue:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RequestsQueue, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.requests = []

    def push_request(self, service_name, request):
        new_req = {service_name: request}
        self.requests.append(new_req)

    def pop_request(self):
        if len(self.requests) > 0:
            cur_req = self.requests.pop(0)
        else:
            cur_req = None
        return cur_req
