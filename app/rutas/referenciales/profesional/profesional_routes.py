from flask import Blueprint, render_template

profmod = Blueprint('profesional', __name__, template_folder='templates')

@profmod.route('/profesional-index')
def profesionalIndex():
    return render_template('profesional-index.html')