# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
    'skoba': 'sqlite:///' + os.path.join(basedir, 'skoba.db'),
    'k188': 'sqlite:///' + os.path.join(basedir, 'k188.db'),
    'sjim': 'sqlite:///' + os.path.join(basedir, 'sjim.db'),
    'mufta': 'sqlite:///' + os.path.join(basedir, 'mufta.db'),
    'rezka': 'sqlite:///' + os.path.join(basedir, 'rezka.db'),
    'stamp': 'sqlite:///' + os.path.join(basedir, 'stamp.db'),
    'packing': 'sqlite:///' + os.path.join(basedir, 'packing.db'),
    'flag': 'sqlite:///' + os.path.join(basedir, 'flag.db')
    }