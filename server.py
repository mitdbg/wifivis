#!/home/sirrice/code/bin/python

try:
  activate_this = './bin/activate_this.py'
  execfile(activate_this, dict(__file__=activate_this))
except:
  pass


import click
import sys
import os
import re
import time
import json
import md5
import pdb
import random
import psycopg2
import traceback
import numpy as np

from functools import wraps
from collections import *
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from flask.ext.compress import Compress


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
print tmpl_dir
app = Flask(__name__, template_folder=tmpl_dir)
Compress(app)

@app.route('/', methods=["POST", "GET"])
def index():
  return render_template("index.html")




@click.command()
@click.option('--debug', is_flag=True)
@click.option('--threaded', is_flag=True)
@click.argument('HOST', default='localhost')
@click.argument('PORT', default=8111, type=int)
def run(debug, threaded, host, port):
  HOST, PORT = host, port
  print "running on %s:%d" % (HOST, PORT)

  app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  try:
    from tornado .wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    print "running tornado server"
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(PORT, address=HOST)
    IOLoop.instance().start()
  except Exception as e:
    print e
    try:
      
      from gevent.wsgi import WSGIServer
      print "running gevent server"
      http_server = WSGIServer((HOST, PORT), app)
      http_server.serve_forever()
    except:
      app.debug = True
      print "running flask server"
      app.run(host=HOST, port=PORT, debug=debug)


if __name__ == '__main__':
  run()
