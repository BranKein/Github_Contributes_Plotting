from flask import Flask
from flask import render_template
from flask_cors import CORS
from contributes import contribute_blueprint
from htmlmin import minify

app = Flask(__name__)
CORS(app)

app.secret_key = 'dsf654fds509654h654jyjhhg654ghj45tr489erew'
app.register_blueprint(contribute_blueprint, url_prefix='/contribute')


@app.route('/')
def root():
    return minify(render_template('index.html'), remove_comments=True, remove_empty_space=True)


if __name__ == '__main__':
    app.run()
