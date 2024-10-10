from flask import Blueprint, render_template

tipcmod = Blueprint('tipodeconsulta', __name__, template_folder='templates')

@tipcmod.route('/tipodeconsulta-index')
def tipodeconsultaIndex():
    return render_template('tipodeconsulta-index.html')