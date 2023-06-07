from flask import Flask

from grathana.views import bp


app = Flask(__name__)
app.register_blueprint(bp)


