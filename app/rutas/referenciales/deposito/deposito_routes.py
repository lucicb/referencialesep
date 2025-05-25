# app/rutas/referenciales/deposito/deposito_routes.py
from flask import Blueprint, render_template

# Definir el Blueprint
depomod = Blueprint('deposito', __name__, template_folder='templates')

# Definir una ruta de ejemplo
@depomod.route('/deposito-index')
def depositoIndex():
    return render_template('deposito-index.html')







