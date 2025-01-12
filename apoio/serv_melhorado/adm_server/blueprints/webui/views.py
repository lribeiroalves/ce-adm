""" Desenvolvimento das views que serão disponibilizadas ao usuário por meio das urls """

from flask import render_template


# HOMEPAGE
def index():
    return render_template('homepage/index.html')
