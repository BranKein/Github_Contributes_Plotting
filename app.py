from flask import Flask, redirect, url_for
from flask import render_template as raw_render_template
from flask_cors import CORS
from contributes import contribute_blueprint
from htmlmin import minify

app = Flask(__name__)
CORS(app)

app.secret_key = 'be646d0f29314d179b70c741b9e6fb49b904f83ad958c94d'

app.register_blueprint(contribute_blueprint, url_prefix='/contribute')


def render_template(*args, **kwargs):
    return minify(raw_render_template(*args, **kwargs), remove_comments=True, remove_empty_space=True)


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
