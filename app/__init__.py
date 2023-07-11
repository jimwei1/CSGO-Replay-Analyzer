from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.index import index_bp
    from app.routes.upload import upload_bp
    from app.routes.parquet import parquet_bp
    from app.routes.radar import radar_bp
    from app.routes.game_state import game_state_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(parquet_bp)
    app.register_blueprint(radar_bp)
    app.register_blueprint(game_state_bp)

    return app
