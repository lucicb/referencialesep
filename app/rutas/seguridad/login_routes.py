from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.dao.referenciales.usuario.login_dao import LoginDao

logmod = Blueprint('login', __name__, template_folder='templates')

@logmod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_nombre = request.form.get('usuario_nombre', '').strip()
        usuario_clave = request.form.get('usuario_clave', '')

        if not usuario_nombre or not usuario_clave:
            flash('Debe completar todos los campos', 'warning')
            return redirect(url_for('login.login'))

        login_dao = LoginDao()
        usuario_encontrado = login_dao.buscarUsuario(usuario_nombre)

        if usuario_encontrado and 'usu_nick' in usuario_encontrado:
            password_hash_del_usuario = usuario_encontrado['usu_clave']

            #if check_password_hash(password_hash_del_usuario, usuario_clave): no se implemento el hasheo de claves
            if (password_hash_del_usuario==usuario_clave):
                session.clear()
                session.permanent = True
                session['usu_id'] = usuario_encontrado.get('usu_id')
                session['usuario_nombre'] = usuario_encontrado.get('usu_nick', '')
                session['nombre_persona'] = usuario_encontrado.get('nombre_persona', '')
                session['grupo'] = usuario_encontrado.get('grupo', '')

                return redirect(url_for('login.inicio'))
            else:
                flash('Contraseña incorrecta', 'warning')
        else:
            flash('Usuario no encontrado', 'warning')

        return redirect(url_for('login.login'))

    return render_template('login.html')

@logmod.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'warning')
    return redirect(url_for('login.login'))

@logmod.route('/')
def inicio():
    if 'usuario_nombre' in session:
        return render_template('inicio.html')
    return redirect(url_for('login.inicio'))