from flask import Blueprint


def register_blueprints(app):
    from .home import home_bp
    from .insights import insights_bp
    from .items import items_bp
    app.register_blueprint(items_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(insights_bp)