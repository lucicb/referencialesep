from flask import Blueprint, render_template

tippmod = Blueprint('tipodepago', __name__, template_folder='templates')

@tippmod.route('/tipodepago-index')
def tipodepagoIndex():
    return render_template('tipodepago-index.html')