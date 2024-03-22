from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for,g,flash
from app_consultorio.auth import login_required
from flask_login import current_user
from datetime import datetime
from .models import *
from .extensions import db

bp = Blueprint('views', __name__, url_prefix='/')

@bp.route('/home')
@login_required
def home():
    return render_template('index.html')

@bp.route('/pacientes')
@login_required
def pacientes():
    patients = Patient.query.all()
    return render_template('paciente/pacientes.html', patients = patients)

@bp.route('/calendario')
@login_required
def calendario():
    return render_template('calendario.html')


@bp.route('/create_paciente', methods=('GET', 'POST'))
@login_required
def create_pacient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        disease = request.form['disease']
        
        # Obtener el ID del médico actualmente autenticado
        doctor_id = g.user.id
       # Creando una nueva instancia del modelo Paciente con los datos capturados
        new_paciente = Patient(name=name, age=age, gender=gender, address=address, doctor_id=doctor_id)
        
        # Guardando el nuevo paciente en la base de datos
        db.session.add(new_paciente)
        db.session.commit()

         # Obteniendo el ID del paciente recién agregado
        patient_id = new_paciente.id
        
        # Creando una nueva instancia del modelo HealthHistory con los datos capturados
        diagnosis_date = datetime.now().date()
        new_health_history = HealthHistory(patient_id=patient_id, disease=disease, diagnosis_date=diagnosis_date)
        
        # Guardando el nuevo historial de salud en la base de datos
        db.session.add(new_health_history)
        db.session.commit()
        return redirect(url_for('views.pacientes'))
        
    return render_template('paciente/add_paciente.html')


def get_paciente(id):
    paciente =  Patient.query.get_or_404(id)
    return paciente

@bp.route('/edit_paciente/<int:patient_id>', methods=('GET', 'POST'))
@login_required
def edit(patient_id):
    # Buscar el paciente por su ID
    paciente = Patient.query.get(patient_id)

    if request.method == 'POST':
        # Actualizar la información del paciente con los datos del formulario
        paciente.name = request.form['name']
        paciente.age = request.form['age']
        paciente.gender = request.form['gender']
        paciente.address = request.form['address']

        # Guardar los cambios en la base de datos
        db.session.commit()

        # Redirigir a la página de detalles del paciente
        return redirect(url_for('views.pacientes', patient_id=patient_id))

    # Renderizar el formulario de edición con los datos actuales del paciente
    return render_template('paciente/edit_paciente.html', paciente=paciente)

@bp.route('/delete_paciente/<int:patient_id>', methods=('POST',))
@login_required
def delete(patient_id):
    # Buscar el paciente por su ID
    paciente = Patient.query.get(patient_id)

    if not paciente:
        # Si el paciente no existe, retornar un error o redirigir a una página de error
        return "Paciente no encontrado", 404

    # Eliminar el historial de salud del paciente (HealthHistory) de la base de datos
    HealthHistory.query.filter_by(patient_id=patient_id).delete()


    # Eliminar el paciente de la base de datos
    db.session.delete(paciente)
    db.session.commit()

    # Redirigir a una página de confirmación o a la página de inicio
    return redirect(url_for('views.pacientes'))

@bp.route('/patient_details/<int:patient_id>')
@login_required
def patient_details(patient_id):
    # Buscar el paciente en la base de datos
    patient = Patient.query.get(patient_id)
    
    if patient is None:
        # Manejar el caso donde el paciente no existe
        return "Paciente no encontrado", 404
    
    # Obtener el historial de salud asociado al paciente
    health_history = HealthHistory.query.filter_by(patient_id=patient_id).all()
    
    return render_template('paciente/patient_details.html', patient=patient, health_history=health_history)


@bp.route('/reservar_turno', methods=['GET','POST'])
@login_required
def reservar_turno():
    
    # Aquí obtienes el ID del médico
    medico = User.query.first()

    if request.method == 'POST':
        nombre_paciente = request.form['nombre_paciente']
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        hora = datetime.strptime(request.form['hora'], '%H:%M').time()
        
        # Buscar al paciente por su nombre
        paciente = Patient.query.filter_by(name=nombre_paciente).first()
        
        if paciente:
            # Encontramos al paciente, procedemos a crear el turno
            nuevo_turno = Turno(paciente_id=paciente.id, medico_id=medico.id, fecha=fecha, hora=hora)
            db.session.add(nuevo_turno)
            db.session.commit()
            return redirect(url_for('views.reservar_turno'))
        else:
            # El paciente no fue encontrado, puedes manejar esto de la manera que prefieras
            flash('Paciente no encontrado')
            return redirect(url_for('views.reservar_turno'))
    else:
        return render_template('turnos.html')

@bp.route('/mostrar_turnos', methods=['GET'])
def mostrar_turnos():
    turnos_guardados = Turno.query.all()
    return render_template('mostrar_turnos.html', turnos_guardados=turnos_guardados)