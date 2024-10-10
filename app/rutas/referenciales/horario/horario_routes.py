from flask import Blueprint, render_template

horamod = Blueprint('horario', __name__, template_folder='templates')

@horamod.route('/horario-index')
def horarioIndex():
    return render_template('horario-index.html')