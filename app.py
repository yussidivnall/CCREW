import asyncio
import threading
from flask import Flask
import track
import alert


def track_job(loop):
    track.initialise()
    loop.run_until_complete(track.connect_ais_stream())


def alert_job(loop):
    loop.run_until_complete(alert.run())


# Application Factory
def create_app(config_name=None):
    """
    Application factory function for creating a Flask app instance.

    Args:
        config_name (str): The configuration name to use (e.g., 'development', 'production').

    Returns:
        app (Flask): The Flask app instance.
    """
    app = Flask(__name__)
    # Track vessels and update CSVs
    tracking_loop = asyncio.new_event_loop()
    tracking_thread = threading.Thread(target=track_job, args=(tracking_loop,))
    tracking_thread.daemon = True
    tracking_thread.start()

    # Inspect CSVs and send alerts
    alerting_loop = asyncio.new_event_loop()
    alerting_thread = threading.Thread(target=alert_job, args=(alerting_loop,))
    alerting_thread.daemon = True
    alerting_thread.start()

    @app.route("/")
    def index():
        return "Hello, World!"

    @app.route("/health")
    def health():
        return {"updated": track.state["last_updated"]}

    return app


# Main function to run the app
if __name__ == "__main__":
    app = create_app("development")
    app.run(host="0.0.0.0", port=5000, debug=True)
