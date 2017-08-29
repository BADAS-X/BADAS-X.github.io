import markdown
import bleach
from bleach import sanitizer
import glob
from flask import Flask, request, escape, abort
from flask import Markup, flash
from flask import url_for, render_template, redirect
from io import BytesIO
from flask_cas import CAS, login_required, login, logout
import datetime

application = Flask(__name__)
cas = CAS()
cas.init_app(application)
application.config['CAS_SERVER'] = "https://cas.binets.fr/"
application.config['CAS_LOGIN_ROUTE'] = '/login'
application.config['CAS_AFTER_LOGIN'] = '/index'


import sqlite3
application.config.from_object(__name__)

moisLettres = [
    'janvier','février','mars',
    'avril','mai','juin',
    'juillet','août','septembre',
    'octobre','novembre','décembre'
]

application.secret_key = open("secret.key",'rb').read()

@application.route('/index')
@application.route('/')
def index():
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])

    allowed_tags = ['a','abbr','b','br','blockquote','code','em','i','li','ol','pre','strong','ul','h1','h2','h3','h4','h5','h6','p','iframe']
    
    allowed_attr = sanitizer.ALLOWED_ATTRIBUTES
    allowed_attr[u'iframe'] = [u'width',u'height',u'src',u'frameborder']

    
    about_file = open('about.md','r',encoding='utf-8')
    about = Markup(md.convert(about_file.read()))
    md.reset()

    posts = []
    for fil in glob.glob('posts/*.md'):
        md.reset()

        html = bleach.clean(md.convert(open(fil,'r',encoding='utf-8').read()),
                tags=allowed_tags)
        curpost = md.Meta
       
        curpost['html'] = Markup(html)
        dd,mm,aaaa = tuple(curpost['date'][0].split('/'))
        curpost['date'] = (int(dd),int(mm)-1,int(aaaa))

        posts.append(curpost)

    sorted(posts, key=lambda pos: pos['date'])
    posts.reverse()
    return render_template("/index.html", about=about, posts=posts, moisLettres=moisLettres, session=cas,
    login=login,logout=logout)

application.debug = True


if __name__ == "__main__":
    application.debug = False
    application.run()
