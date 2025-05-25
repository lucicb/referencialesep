# deposito_api.py
@pdcmod.route('/get_depositos', methods=['GET'])
def get_depositos():
    deposito_dao = DepositoDao()

    try:
        # Obtener todos los depósitos
        depositos = deposito_dao.get_all_depositos()

        return jsonify({'depositos': depositos})

    except Exception as e:
        app.logger.error(f"Error al obtener depósitos: {str(e)}")
        return jsonify({'depositos': []}), 500




