from flask import Flask, render_template, request

app = Flask(__name__)

# simulacion de datos en memoria
EQUIPOS = []
INSCRIPCIONES_CLUBES = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/campeonato', methods=['GET', 'POST'])
def campeonato():
    msg = None
    error = None
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        ciudad = request.form.get('ciudad', '').strip()
        genero = request.form.get('genero', '').strip()
        integrantes = request.form.get('integrantes', '').strip()

        # Validaciones
        if not nombre or not ciudad or not genero or not integrantes:
            error = 'Por favor completa todos los campos.'
        elif ciudad.lower() != 'quito':
            error = 'Solo se permiten equipos de la ciudad de Quito.'
        elif genero not in ['Femenina', 'Masculina']:
            error = 'Categoría inválida.'
        else:
            lista_integrantes = [x.strip() for x in integrantes.split(',') if x.strip()]
            if len(lista_integrantes) < 5 or len(lista_integrantes) > 12:
                error = 'El equipo debe tener entre 5 y 12 integrantes.'
            elif any(eq['nombre'].lower() == nombre.lower() for eq in EQUIPOS):
                error = 'Ya existe un equipo con ese nombre.'
            else:
                EQUIPOS.append({
                    'nombre': nombre,
                    'ciudad': ciudad,
                    'genero': genero,
                    'integrantes': ', '.join(lista_integrantes)
                })
                msg = '¡Equipo inscrito correctamente!'

    return render_template('campeonato.html', equipos=EQUIPOS, msg=msg, error=error)

@app.route('/manana')
def manana():
    return render_template('manana.html')

@app.route('/clubes', methods=['GET', 'POST'])
def clubes():
    msg = None
    CLUBES_LIST = [
        {'nombre': 'Yoga', 'modalidad': 'Virtual', 'coach': 'Andrea Pérez', 'horario': 'Jueves 17:00-18:00', 'ubicacion': 'Teams'},
        {'nombre': 'Running', 'modalidad': 'Presencial (Quito)', 'coach': 'Juan Pérez', 'horario': 'Martes y Jueves 18:30-19:30', 'ubicacion': 'La Carolina'},
        {'nombre': 'Lectura', 'modalidad': 'Híbrido', 'coach': 'Pedro Pérez', 'horario': 'Miércoles 17:00-18:00', 'ubicacion': 'Teams / Sala Creando Más'}
    ]
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        club = request.form.get('club', '').strip()
        rol = request.form.get('rol', '').strip()
        #validacion (esto es escalable)
        if not nombre or not club or not rol:
            msg = "Por favor completa todos los campos."
        else:
            INSCRIPCIONES_CLUBES.append({
                'nombre': nombre,
                'club': club,
                'rol': rol
            })
            msg = '¡Inscripción enviada correctamente!'
    return render_template('clubes.html', clubes=CLUBES_LIST, msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
