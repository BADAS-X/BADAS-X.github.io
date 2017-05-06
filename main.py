import markdown
import glob
from flask import Flask, request, escape, abort
from flask import Markup
from flask import url_for, render_template, redirect
from io import BytesIO
from flask_cas import CAS, login_required

app = Flask(__name__)
cas = CAS(app)
app.config['CAS_SERVER'] = "https://cas.binets.fr/"
app.config['CAS_AFTER_LOGIN'] = 'index'
app.config['CAS_LOGIN_ROUTE'] = '/cas'
app.config['CAS_LOGOUT_ROUTE'] = '/cas/logout'


import sqlite3
app.config.from_object(__name__)


@app.route('/index')
@app.route('/')
def index():
    tmpl = "/index.html"
    aboutfile = open('about.md', 'r', encoding='utf-8')
    about = Markup(markdown.markdown(text=aboutfile.read()))

    posts = []
    for fil in glob.glob('posts/*.md'):
        posts.append(
            Markup(markdown.markdown(
                text=open(fil, 'r', encoding='utf-8').read()
            )
            )
        )

    return render_template(tmpl, about=about, posts=posts)

app.debug = True


if __name__ == "__main__":
    app.threaded = True
    app.debug = True
    app.run()
