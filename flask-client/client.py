import requests
import time
from opentracing_instrumentation.client_hooks import install_all_patches
from jaeger_client import Config

from os import getenv

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')
WEBSERVER_HOST = getenv('WEBSERVER_HOST', 'localhost')

config = Config(config={'sampler': {'type': 'const', 'param': 1},
                        'logging': True,
                        'local_agent': {'reporting_host': JAEGER_HOST}},
                service_name="jaeger-opentracing-client")
tracer = config.initialize_tracer()

install_all_patches()

while True:
    url = "http://{}:5000/log".format(WEBSERVER_HOST)
    try:
        requests.get(url)
    except:
        print("ERR_CONNECTION_TIMED_OUT")

    time.sleep(2)
    tracer.close()