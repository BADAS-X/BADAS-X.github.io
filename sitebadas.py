import markdown
import glob
from flask import Flask, request, escape, abort
from flask import Markup
from flask import url_for, render_template, redirect
from io import BytesIO
from flask_cas import CAS, login_required
import datetime

application = Flask(__name__)
cas = CAS(application)
application.config['CAS_SERVER'] = "https://cas.binets.fr/"
application.config['CAS_AFTER_LOGIN'] = 'index'
application.config['CAS_LOGIN_ROUTE'] = '/cas'
application.config['CAS_LOGOUT_ROUTE'] = '/cas/logout'



import sqlite3
application.config.from_object(__name__)

moisLettres = {
    1:'janvier',
    2:'février',
    3:'mars',
    4:'avril',
    5:'mai',
    6:'juin',
    7:'juillet',
    8:'août',
    9:'septembre',
    10:'octobre',
    11:'novembre',
    12:'décembre'
}

@application.route('/index')
@application.route('/')
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
        curpost['date'] = tuple(int(val) for val in (curpost['date'][0]).split('/'))

        posts.append(curpost)

    sorted(posts, key=lambda pos: pos['date'],
        reverse=True)


    return render_template("/index.html", about=about, posts=posts, moisLettres=moisLettres, session=cas)

application.debug = True


if __name__ == "__main__":
    application.threaded = True
    application.debug = False
    application.run()
