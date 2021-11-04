import logging
from jaeger_client import Config
from flask import Flask
from flask_opentracing import FlaskTracing
from os import getenv

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')
JAEGER_PORT = getenv('JAEGER_PORT', 6831)

if __name__ == '__main__':
        app = Flask(__name__)
        log_level = logging.DEBUG
        logging.getLogger('').handlers = []
        logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

        config = Config(config={'sampler': {'type': 'const', 'param': 1},
                                'logging': True,
                                'local_agent':
                                {'reporting_host': JAEGER_HOST, 'reporting_port': 6831 }},
                        service_name="jaeger-opentracing-server")
        jaeger_tracer = config.initialize_tracer()
        tracing = FlaskTracing(jaeger_tracer)

        @app.route('/log')
        @tracing.trace()
        def log():
                with jaeger_tracer.start_active_span(
                        'python webserver internal span of log method') as scope:
                        
                    a = 1
                    b = 2
                    c = a + b

                    scope.span.log_kv({'event': 'my computer knows math!', 'result': c})

                    return "log"

        app.run(debug=True, host='0.0.0.0', port=5000)