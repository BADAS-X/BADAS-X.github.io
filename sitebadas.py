import markdown
import bleach
from bleach import sanitizer
import glob
from flask import Flask, request, escape, abort, Markup, flash, g, url_for, render_template, redirect
from flask_babel import Babel, gettext
from flask_cas import CAS, login_required, login, logout
from models import BabelConfig

application = Flask(__name__)

application.secret_key = open("secret.key",'rb').read()

cas = CAS(application)
babel = Babel(application)
application.config.from_object(BabelConfig)


@babel.localeselector
def get_locale():
    browser = request.accept_languages.best_match(BabelConfig.SUPPORTED_LANGUAGES.keys())
    return browser


moisLettres = [
    'jan','fév','mars',
    'avr','mai','juin',
    'jui','août','sep',
    'oct','nov','déc'
]



@application.route('/')
def index():
    CONTENT_PATH = "content/" + get_locale() + "/"

    md = markdown.Markdown(extensions=['markdown.extensions.meta'])

    allowed_tags = ['a','abbr','b','br','blockquote','code','em','i','img','li','ol','pre','strong','ul','h1','h2','h3','h4','h5','h6','p','iframe']

    allowed_attr = sanitizer.ALLOWED_ATTRIBUTES
    allowed_attr[u'iframe'] = [u'width',u'height',u'src',u'frameborder']
    allowed_attr[u'img'] = [u'width',u'height',u'src']

    about_file = open(CONTENT_PATH + 'about.md','r',encoding='utf-8')
    about = Markup(md.convert(about_file.read()))
    md.reset()

    posts = []
    for fil in glob.glob(CONTENT_PATH+'posts/*.md'):
        md.reset()

        html = bleach.clean(md.convert(open(fil,'r',encoding='utf-8').read()),
                tags=allowed_tags)
        curpost = md.Meta

        curpost['html'] = Markup(html)
        dd,mm,aaaa = map(int, curpost['date'][0].split('/'))
        curpost['date'] = (aaaa, mm - 1, dd)

        posts.append(curpost)

    posts.sort(key=lambda pos: pos['date'], reverse=True)
    return render_template("/index.html", about=about, posts=posts, moisLettres=moisLettres, session=cas,
    login=login,logout=logout)


if __name__ == "__main__":
    application.debug = False
    application.run()
