from flask import Blueprint, render_template

sucurmod = Blueprint('sucursal', __name__, template_folder='templates')

@sucurmod.route('/sucursal-index')
def sucursalIndex():
    return render_template('sucursal-index.html')