#/usr/bin/env python
#coding=utf-8

"""
    Xiangnan facemash Web-related components.
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Lope group is working on this."


def main():
    app.run()
