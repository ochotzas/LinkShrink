from app import app
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the LinkShrink web application')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=5000, help='Port number to run the server on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--threaded', action='store_true', help='Enable threaded mode')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug, threaded=args.threaded)
