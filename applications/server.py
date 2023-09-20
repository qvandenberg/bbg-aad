from aad_pricing import index
from aad_pricing.index import dash_app as application

# needed for gunicorn/wsgi to connect
server = application.server

if __name__ == "__main__":
    application.run(debug=False)
