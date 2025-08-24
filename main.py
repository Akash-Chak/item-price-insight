from flask import Flask
from pages import register_blueprints


def create_app(config: dict = {}):
    app = Flask(__name__)
    app.config.update({} if config is None else config)

    register_blueprints(app)

    return app


if __name__ == '__main__':
    app = create_app({'DEBUG': True})
    app.run(host='0.0.0.0', port=5000)