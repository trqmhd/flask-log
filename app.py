import flask, socket
import json, os
import logging.config
from flask import has_request_context, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

if not os.path.exists("log"):
    os.mkdir("log")

with open("logging.json", "r") as f:
    configInfo = json.load(f)
logging.config.dictConfig(configInfo)

logger = logging.getLogger(__name__)

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    if has_request_context():
        record.request_method = request.method
        record.ip = socket.gethostname()
    else:
        record.request_method = "SYS"
        record.ip = "localhost"
    return record

old_factory = logging.getLogRecordFactory()
logging.setLogRecordFactory(record_factory)

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

@app.route('/', methods=['GET'])
def home():
    logger.info("Flask app is working ....." )
    logger.debug("Debug mode is off .....")
    logger.error("There is no error .....")
    return "<h1> Home Page </p>"

app.run()