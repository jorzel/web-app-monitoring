import random
import time

from flask import Flask, request
from prometheus_client import Histogram, make_wsgi_app
from werkzeug import Response
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})


HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration",
    "Requests durations",
    ["method", "url", "code"],
)


def observe_http(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        end = time.time()
        HTTP_REQUEST_DURATION.labels(
            method=request.method,
            code=response.status_code,
            url=request.url,
        ).observe(end - start)
        return response

    return wrapper


@app.route("/synthetic")
@observe_http
def synthetic():
    random_duration = (
        random.choice([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3])
        * random.randint(1, 100)
        * 0.001
    )
    time.sleep(random_duration)

    response_code = random.choice([200, 200, 200, 200, 200, 400, 401, 500])
    return Response(str(response_code), status=response_code)


@app.route("/")
@app.route("/up")
def up():
    return "I am running"
