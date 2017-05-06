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
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])


    aboutfile = open('about.md','r',encoding='utf-8')
    about = Markup(md.convert(aboutfile.read()))
    md.reset()

    posts = []
    for fil in glob.glob('posts/*.md'):
        md.reset()

        html = Markup(
                md.convert(open(fil,'r',encoding='utf-8').read())
                )
        curpost = md.Meta
        curpost['html'] = html

        posts.append(curpost)


    return render_template("/index.html", about=about, posts=posts)

app.debug = True


if __name__ == "__main__":
    app.threaded=True
    app.debug=True
    app.run()
