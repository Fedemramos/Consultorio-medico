from app_consultorio import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique = True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    # Relación uno a muchos con pacientes
    patients = db.relationship('Patient', backref='doctor', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
      return f"Users('{self.username}', '{self.password}')" 


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(20), nullable=True)
  
    # Columna para almacenar el ID del doctor (usuario) asociado
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 
    # Relación uno a muchos con el historial de salud
    health_history = db.relationship('HealthHistory', backref='patient', uselist=False, lazy=True)

    def __init__(self, name, age, gender, doctor_id, address=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.doctor_id = doctor_id
        self.address = address

    def __repr__(self):
        return f"Patient('{self.name}', '{self.age}', '{self.gender}', '{self.address}')"

class HealthHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), unique=True, nullable=False)
    # Campos para el historial de salud
    disease = db.Column(db.String(400), nullable=False)
    diagnosis_date = db.Column(db.Date, nullable=False)
   

    def __init__(self, patient_id, disease, diagnosis_date):
        self.patient_id = patient_id
        self.disease = disease
        self.diagnosis_date = diagnosis_date

    def __repr__(self):
        return f"HealthHistory('{self.disease}', '{self.diagnosis_date}')"
    

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    paciente = db.relationship('Patient', backref=db.backref('turnos_reservados', lazy=True))
    medico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medico = db.relationship('User', backref=db.backref('turnos_asignados', lazy=True))
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)