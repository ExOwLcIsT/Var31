from datetime import datetime, timedelta
import random
from bson import ObjectId
from flask import Flask,  render_template, session
from routes.collections import collections_bp
from routes.documents import documents_bp
from routes.login import login_bp
from routes.fields import fields_bp
app = Flask(__name__)

app.register_blueprint(collections_bp, url_prefix='/api')
app.register_blueprint(documents_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(fields_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def get_index_page():
    return render_template(
        "index.html"
    )


@app.route('/login', methods=['GET'])
def get_login_page():
    return render_template(
        "login.html"
    )

if __name__ == '__main__':
    app.run(debug=True)
