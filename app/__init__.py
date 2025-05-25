from datetime import timedelta
from flask import Flask

app = Flask(__name__)

# Inicializar secret key
app.secret_key = b'_5#y2L"F6Q7z\n\xec]'

# Establecer duración de sesión, 15 minutos
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Importar módulo de seguridad
from app.rutas.seguridad.login_routes import logmod
app.register_blueprint(logmod)

# Importar las rutas de referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod  # ciudad
from app.rutas.referenciales.paises.pais_routes import paimod   # pais
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import naciomod  # nacionalidad
from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod  # estado civil
# from app.rutas.referenciales.sexo.sexo_routes import sexmod  # sexo (comentado, si no lo usas)
from app.rutas.referenciales.persona.persona_routes import persmod  # persona
from app.rutas.referenciales.dia.dia_routes import diamod  # dia
from app.rutas.referenciales.turno.turno_routes import turmod  # turno
from app.rutas.referenciales.horario.horario_routes import horamod  # horario
# from app.rutas.referenciales.sucursal.sucursal_routes import sucurmod  # sucursal (comentado, si no lo usas)
from app.rutas.referenciales.profesional.profesional_routes import profmod  # profesional
# from app.rutas.referenciales.tipodepago.tipodepago_routes import tippmod  # tipodepago (comentado, si no lo usas)
from app.rutas.referenciales.tipodeconsulta.tipodeconsulta_routes import tipcmod  # tipodeconsulta
from app.rutas.referenciales.cargo.cargo_routes import carmod  # cargo
from app.rutas.referenciales.departamento.departamento_routes import depmod  # departamento
from app.rutas.referenciales.deposito.deposito_routes import depomod

# Importar gestionar compras
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedidos_compras_routes import pdcmod

# Registrar las rutas de referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')  # ciudad
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises')  # pais
app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')  # nacionalidad
app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')  # estado civil
# app.register_blueprint(sexmod, url_prefix=f'{modulo0}/sexo')  # sexo (comentado)
app.register_blueprint(persmod, url_prefix=f'{modulo0}/persona')  # persona
app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia')  # dia
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno')  # turno
app.register_blueprint(horamod, url_prefix=f'{modulo0}/horario')  # horario
# app.register_blueprint(sucurmod, url_prefix=f'{modulo0}/sucursal')  # sucursal (comentado)
app.register_blueprint(profmod, url_prefix=f'{modulo0}/profesional')  # profesional
# app.register_blueprint(tippmod, url_prefix=f'{modulo0}/tipodepago')  # tipodepago (comentado)
app.register_blueprint(tipcmod, url_prefix=f'{modulo0}/tipodeconsulta')  # tipodeconsulta
app.register_blueprint(carmod, url_prefix=f'{modulo0}/cargo')  # cargo
app.register_blueprint(depmod, url_prefix=f'{modulo0}/departamento')  # departamento
app.register_blueprint(depomod, url_prefix=f'{modulo0}/deposito')  # deposito

# Registrar las rutas de gestionar compras
modulo1 = '/gestionar-compras'
app.register_blueprint(pdcmod, url_prefix=f'{modulo1}/registrar-pedido-compras')  # registrar pedidos compras

# Registrar las APIs
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.paises.pais_api import paisapi
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacioapi
from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi
# from app.rutas.referenciales.sexo.sexo_api import sexapi  # sexo (comentado)
from app.rutas.referenciales.persona.persona_api import persapi
from app.rutas.referenciales.dia.dia_api import diaapi
from app.rutas.referenciales.turno.turno_api import turnoapi
from app.rutas.referenciales.horario.horario_api import horaapi
# from app.rutas.referenciales.sucursal.sucursal_api import sucurapi  # sucursal (comentado)
from app.rutas.referenciales.profesional.profesional_api import profapi
# from app.rutas.referenciales.tipodepago.tipodepago_api import tippapi  # tipodepago (comentado)
from app.rutas.referenciales.tipodeconsulta.tipodeconsulta_api import tipcapi
from app.rutas.referenciales.cargo.cargo_api import carapi
from app.rutas.referenciales.departamento.departamento_api import depapi
from app.rutas.referenciales.deposito.deposito_api import depoapi
from app.rutas.referenciales.sucursal.sucursal_api import sucapi
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api import pdcapi

# Registrar las APIs v1
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=f'{version1}/ciudad')  # ciudad
app.register_blueprint(paisapi, url_prefix=f'{version1}/paises')  # pais
app.register_blueprint(nacioapi, url_prefix=f'{version1}/nacionalidad')  # nacionalidad
app.register_blueprint(estacivapi, url_prefix=f'{version1}/estadocivil')  # estado civil
# app.register_blueprint(sexapi, url_prefix=f'{version1}/sexo')  # sexo (comentado)
app.register_blueprint(persapi, url_prefix=f'{version1}/persona')  # persona
app.register_blueprint(diaapi, url_prefix=f'{version1}/dia')  # dia
app.register_blueprint(turnoapi, url_prefix=f'{version1}/turno')  # turno
app.register_blueprint(horaapi, url_prefix=f'{version1}/horario')  # horario
# app.register_blueprint(sucurapi, url_prefix=f'{version1}/sucursal')  # sucursal (comentado)
app.register_blueprint(profapi, url_prefix=f'{version1}/profesional')  # profesional
# app.register_blueprint(tippapi, url_prefix=f'{version1}/tipodepago')  # tipodepago (comentado)
app.register_blueprint(tipcapi, url_prefix=f'{version1}/tipodeconsulta')  # tipodeconsulta
app.register_blueprint(carapi, url_prefix=f'{version1}/cargo')  # cargo
app.register_blueprint(depapi, url_prefix=f'{version1}/departamento')  # departamento
app.register_blueprint(depoapi, url_prefix=f'{version1}/deposito')

# Gestionar compras API
apiversion1 = '/api/v1'
app.register_blueprint(pdcapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-pedido-compras')  # registrar pedidos compras
app.register_blueprint(sucapi, url_prefix=f'{apiversion1}/sucursal')  # sucursal

  # deposito

if __name__ == '__main__':
    app.run(debug=True)




