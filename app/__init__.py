from flask import Flask

app = Flask(__name__)

# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod #ciudad
from app.rutas.referenciales.paises.pais_routes import paimod   #pais
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import naciomod  #nacionalidad
from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod  #estado civil
from app.rutas.referenciales.sexo.sexo_routes import sexmod  #sexo
from app.rutas.referenciales.persona.persona_routes import persmod  #persona
from app.rutas.referenciales.dia.dia_routes import diamod  #dia
from app.rutas.referenciales.turno.turno_routes import turmod  #turno
from app.rutas.referenciales.horario.horario_routes import horamod #horario
from app.rutas.referenciales.sucursal.sucursal_routes import sucurmod #sucursal
from app.rutas.referenciales.profesional.profesional_routes import profmod #profesional
from app.rutas.referenciales.tipodepago.tipodepago_routes import tippmod #tipodepago
from app.rutas.referenciales.tipodeconsulta.tipodeconsulta_routes import tipcmod #tipodeconsulta
from app.rutas.referenciales.cargo.cargo_routes import carmod #cargo 



# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad') #ciudad
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises') #pais
app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')  #nacionalidad
app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')  #estado civil
app.register_blueprint(sexmod, url_prefix=f'{modulo0}/sexo')  #sexo
app.register_blueprint(persmod, url_prefix=f'{modulo0}/persona') #persona
app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia') #dia
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno') #turno
app.register_blueprint(horamod, url_prefix=f'{modulo0}/horario') 
app.register_blueprint(sucurmod, url_prefix=f'{modulo0}/sucursal')
app.register_blueprint(profmod, url_prefix=f'{modulo0}/profesional')
app.register_blueprint(tippmod, url_prefix=f'{modulo0}/tipodepago')
app.register_blueprint(tipcmod, url_prefix=f'{modulo0}/tipodeconsulta')
app.register_blueprint(carmod, url_prefix=f'{modulo0}/cargo')




#ciudad
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi

#pais
from app.rutas.referenciales.paises.pais_api import paisapi

#nacionalidad
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacioapi

#estado civil
from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi

#sexo
from app.rutas.referenciales.sexo.sexo_api import sexapi

#persona
from app.rutas.referenciales.persona.persona_api import persapi

#dia
from app.rutas.referenciales.dia.dia_api import diaapi

#turno
from app.rutas.referenciales.turno.turno_api import turnoapi

#horario
from app.rutas.referenciales.horario.horario_api import horaapi

#sucursal
from app.rutas.referenciales.sucursal.sucursal_api import sucurapi

#profesional
from app.rutas.referenciales.profesional.profesional_api import profapi

#tipo de pago
from app.rutas.referenciales.tipodepago.tipodepago_api import tippapi

#tipo de consulta
from app.rutas.referenciales.tipodeconsulta.tipodeconsulta_api import tipcapi

#cargo
from app.rutas.referenciales.cargo.cargo_api import carapi



# APIS v1
#Ciudad
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)

#Pais
version1 = '/api/v1'
app.register_blueprint(paisapi, url_prefix=version1)

#nacionalidad
version1 = '/api/v1'
app.register_blueprint(nacioapi, url_prefix=version1)

#Estado civil
version1 = '/api/v1'
app.register_blueprint(estacivapi, url_prefix=version1)

#sexo
version1 = '/api/v1'
app.register_blueprint(sexapi, url_prefix=version1)

#persona
version1 = '/api/v1'
app.register_blueprint(persapi, url_prefix=version1)

#dia
version1 = '/api/v1'
app.register_blueprint(diaapi, url_prefix=version1)

#turno
version1 = '/api/v1'
app.register_blueprint(turnoapi, url_prefix=version1)

#horario
version1 = '/api/v1'
app.register_blueprint(horaapi, url_prefix=version1)


#sucursal
version1 = '/api/v1'
app.register_blueprint(sucurapi, url_prefix=version1)

#profesional
version1 = '/api/v1' 
app.register_blueprint(profapi, url_prefix=version1)

#Tipo de pago
version1 = '/api/v1' 
app.register_blueprint(tippapi, url_prefix=version1)

#tipo de consulta
version1 = '/api/v1' 
app.register_blueprint(tipcapi, url_prefix=version1)

#cargo
version1 = '/api/v1' 
app.register_blueprint(carapi, url_prefix=version1)
 

