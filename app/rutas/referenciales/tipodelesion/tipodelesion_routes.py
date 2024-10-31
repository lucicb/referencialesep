from flask import Blueprint, render_template

tiplmod = Blueprint('tipodelesion', __name__, template_folder='templates')

@tiplmod.route('/tipodelesion-index')
def tipodelesionIndex():
    return render_template('tipodelesion-index.html')