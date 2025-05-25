# app/routes/depositos_routes.py

from flask import Blueprint, request, jsonify
from app.dao.referenciales.deposito.deposito_dao import DepositoDao

# Crear un Blueprint para las rutas de depósitos
deposito_mod = Blueprint('deposito_mod', __name__)

# Ruta para obtener los depósitos de una sucursal
@pdcmod.route('/get_depositos', methods=['GET'])
def get_depositos():
    deposito_dao = DepositoDao()
    depositos = deposito_dao.get_all_depositos()  # Aquí obtienes todos los depósitos
    return jsonify({'depositos': depositos})  # Responde con los depósitos en formato JSON





