from quart import Quart
from queue_req.postQueue import postqueueb
from queue_req.healthCheck import healthcheckb

app = Quart(__name__)
app.register_blueprint(postqueueb)
app.register_blueprint(healthcheckb)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8040)
