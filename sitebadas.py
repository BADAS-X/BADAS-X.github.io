import markdown
import bleach
from bleach import sanitizer
import glob
from flask import Flask, request, escape, abort, Markup, flash, g, url_for, render_template, redirect
from flask_babel import Babel
from flask_cas import CAS, login_required, login, logout
from models import BaseConfig


application = Flask(__name__)
cas = CAS(application)
babel = Babel(application)
application.secret_key = open("secret.key",'rb').read()
application.config.from_object(BaseConfig)

@babel.localeselector
def get_locale():
    return g.get('lang_code',app.config['BABEL_DEFAULT_LOCALE'])

moisLettres = [
    'jan','fév','mars',
    'avr','mai','juin',
    'jui','août','sep',
    'oct','nov','déc'
]

@application.url_defaults
def set_lang_code(endpoint, values):
    if 'lang_code' in values or not g.get('lang_code',None):
        return
    if app.url_map.is_endpoint_expecting(endpoint,'lang_code'):
        values['lang_code'] = g.lang_code

@application.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)

@application.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)

@application.route('/fr', endpoint="index_fr")
@application.route('/en', endpoint="index_en")
def index():
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])

    allowed_tags = ['a','abbr','b','br','blockquote','code','em','i','img','li','ol','pre','strong','ul','h1','h2','h3','h4','h5','h6','p','iframe']

    allowed_attr = sanitizer.ALLOWED_ATTRIBUTES
    allowed_attr[u'iframe'] = [u'width',u'height',u'src',u'frameborder']
    allowed_attr[u'img'] = [u'width',u'height',u'src']

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
    return render_template("/index.html", about=about, posts=posts, moisLettres=moisLettres, session=cas,
    login=login,logout=logout)


if __name__ == "__main__":
    application.debug = False
    application.run()
