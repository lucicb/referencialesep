from flask import Blueprint, render_template

depmod = Blueprint('departamento', __name__, template_folder='templates')

@depmod.route('/departamento-index')
def depaartamentoIndex():
    return render_template('departamento-index.html')