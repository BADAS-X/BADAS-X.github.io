Flask-CAS
=========

Flask-CAS is a Flask extension which makes it easy to
authenticate with a CAS.

CAS
===

The Central Authentication Service (CAS) is a single sign-on 
protocol for the web. Its purpose is to permit a user to access 
multiple applications while providing their credentials (such as 
userid and password) only once. It also allows web applications 
to authenticate users without gaining access to a user's security 
credentials, such as a password. The name CAS also refers to a 
software package that implements this protocol. 

(Very short) Setup Tutorial
===========================

First create a Flask instance:

.. code:: python

    from flask import Flask

    app = Flask(__name__)

Apply CAS on your Flask instance:

.. code:: python

    from flask.ext.cas import CAS

    CAS(app)

Do needed configuration:

.. code:: python

    app.config['CAS_SERVER'] = 'https://sso.pdx.edu' 

    app.config['CAS_AFTER_LOGIN'] = 'route_root'

Using
=====

After you setup you will get two new routes `/login/`
and `/logout/`.

Reference documentation
=======================

See https://github.com/cameronbwhite/Flask-CAS

