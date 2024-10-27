from quart import Quart
from queue.postQueue import rollbackrequestb
from queue.healthCheck import healthcheckb

app = Quart(__name__)
app.register_blueprint(rollbackrequestb)
app.register_blueprint(healthcheckb)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8040)
