import markdown
import glob
from flask import Flask, request, session, escape, abort
from flask import Markup
from flask import url_for, render_template, redirect
from flask_login import LoginManager
from io import BytesIO

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

import sqlite3
app.config.from_object(__name__)


@app.route('/index')
@app.route('/')
def index():
    tmpl = "/index.html"
    aboutfile = open('about.md','r',encoding='utf-8')
    about = Markup(markdown.markdown(text=aboutfile.read()))

    postsFiles = glob.glob('posts/*.md')
    posts = []
    for fil in postsFiles:
        posts.append(
            Markup(markdown.markdown(
            text= open(fil, 'r',encoding='utf-8').read()
            )
            )
        )


    return render_template(tmpl, about=about, posts=posts)


app.debug = True


if __name__ == "__main__":
    app.threaded=True
    app.debug=True
    app.run()
