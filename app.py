from flask import Flask, render_template, request, redirect
from forms.patient_form import PatientForm
from forms.symptom_form import SymptomForm
from forms.disease_form import DiseaseForm
from forms.edit_symptom import EditSymptomForm
from forms.edit_disease import EditDiseaseForm
from forms.heart_form import HeartForm
import uuid
import psycopg2
import json
import plotly
from sqlalchemy.sql import func
# import plotly.plotly as py
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
import numpy as np


app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:fastdagger@localhost/milev'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://povekvwdahxoju:69c9598da601f3532f86f58eb4a2a1c46c226698bc7565ecc6e8828e27d44ce6@ec2-54-204-37-92.compute-1.amazonaws.com:5432/d485jnsrf0bpje'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class OrmPatient(db.Model):
    __tablename__ = 'orm_patient'

    patient_id = db.Column(db.Integer, primary_key=True)
    patient_age = db.Column(db.Integer, nullable=False)
    patient_height = db.Column(db.Float, nullable=False)
    patient_weight = db.Column(db.Float, nullable=False)
    patient_temperature = db.Column(db.Float, nullable=False)

    symptom = db.relationship('OrmSymptom')


class OrmSymptom(db.Model):
    __tablename__ = 'orm_symptom'

    symptom_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    patient_id = db.Column(db.Integer, db.ForeignKey('orm_patient.patient_id'))

    disease = db.relationship('OrmDisease')

class OrmDisease(db.Model):
    __tablename__ = 'orm_disease'

    disease_id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(20), nullable=False)
    severity = db.Column(db.Integer, nullable=False)

    symptom_id = db.Column(db.Integer, db.ForeignKey('orm_symptom.symptom_id'))

class OrmHeart(db.Model):
    ___tablename__ = 'orm_heart'

    heart_id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    trestbps = db.Column(db.Float, nullable=False)
    chol= db.Column(db.Float, nullable=False)
    thalach = db.Column(db.Integer, nullable=False)

db.drop_all()

db.create_all()

Lesha = OrmPatient(
    patient_id=1,
    patient_age=43,
    patient_height=190,
    patient_weight=103,
    patient_temperature=37.7
)

Vlad = OrmPatient(
    patient_id=2,
    patient_age=43,
    patient_height=195,
    patient_weight=79,
    patient_temperature=37.7
)

Dima = OrmPatient(
    patient_id=3,
    patient_age=43,
    patient_height=204,
    patient_weight=79,
    patient_temperature=37.7
)

Ivan = OrmPatient(
    patient_id=8,
    patient_age=43,
    patient_height=164,
    patient_weight=79,
    patient_temperature=37.7
)

Jenya = OrmPatient(
    patient_id=9,
    patient_age=19,
    patient_height=160,
    patient_weight=77,
    patient_temperature=37.7
)

Nastya = OrmPatient(
    patient_id=4,
    patient_age=19,
    patient_height=190,
    patient_weight=77,
    patient_temperature=37.7
)

Max = OrmPatient(
    patient_id=5,
    patient_age=20,
    patient_height=166,
    patient_weight=56,
    patient_temperature=36.9
)

Serg = OrmPatient(
    patient_id=6,
    patient_age=29,
    patient_height=196,
    patient_weight=49,
    patient_temperature=37.1
)

Kate = OrmPatient(
    patient_id=7,
    patient_age=43,
    patient_height=163,
    patient_weight=77,
    patient_temperature=37.4
)


testheart = OrmHeart(
    heart_id= 1,
    age= 44,
    sex= 'male',
    trestbps= 110,
    chol= 197,
    thalach=177
)

cough = OrmSymptom(
    symptom_id = 2,
    description = 'cough',
    patient_id=5
)

throat = OrmSymptom(
    symptom_id = 3,
    description = 'throat pain',
    patient_id=5
)

head = OrmSymptom(
    symptom_id = 1,
    description = 'head pain',
    patient_id=6
)

URTI = OrmDisease(
    disease_id=1,
    disease_name='URTI',
    severity=3,
    symptom_id = 2
)

URTI2 = OrmDisease(
    disease_id=2,
    disease_name='URTI',
    severity=3,
    symptom_id =3
)


Flu = OrmDisease(
    disease_id=3,
    disease_name='Flu',
    severity=4,
    symptom_id =2
)

Flu2 = OrmDisease(
    disease_id=4,
    disease_name='Flu',
    severity=4,
    symptom_id = 3
)

Migraine = OrmDisease(
    disease_id=5,
    disease_name='Migraine',
    severity=5,
    symptom_id = 1
)

High_pressure = OrmDisease(
    disease_id=6,
    disease_name='High_pressure',
    severity=3,
    symptom_id = 1
)

Cold = OrmDisease(
    disease_id=7,
    disease_name='Cold',
    severity=3,
    symptom_id = 2
)

Cold2 = OrmDisease(
    disease_id=8,
    disease_name='Cold',
    severity=3,
    symptom_id = 3
)

Croup = OrmDisease(
    disease_id=9,
    disease_name='Croup',
    severity=5,
    symptom_id = 2
)

Croup2 = OrmDisease(
    disease_id=10,
    disease_name='Croup',
    severity=5,
    symptom_id = 1
)

Pertussis = OrmDisease(
    disease_id=11,
    disease_name='Croup',
    severity=5,
    symptom_id = 2
)

testheart2 = OrmHeart(
    heart_id= 2,
    age= 30,
    sex= 'male',
    trestbps= 100,
    chol= 177,
    thalach=160
)

testheart3 = OrmHeart(
    heart_id= 3,
    age= 40,
    sex= 'male',
    trestbps= 90,
    chol= 180,
    thalach=180
)

testheart4 = OrmHeart(
    heart_id= 4,
    age= 20,
    sex= 'female',
    trestbps= 120,
    chol= 190,
    thalach=183
)

testheart5 = OrmHeart(
    heart_id= 5,
    age= 35,
    sex= 'female',
    trestbps= 90,
    chol= 195,
    thalach=175
)

testheart6 = OrmHeart(
    heart_id= 6,
    age= 45,
    sex= 'female',
    trestbps= 95,
    chol= 186,
    thalach=166
)

testheart7 = OrmHeart(
    heart_id= 7,
    age= 42,
    sex= 'male',
    trestbps= 105,
    chol= 176,
    thalach=170
)

testheart8 = OrmHeart(
    heart_id= 8,
    age= 50,
    sex= 'male',
    trestbps= 85,
    chol= 186,
    thalach=180
)


testheart9 = OrmHeart(
    heart_id= 9,
    age= 55,
    sex= 'female',
    trestbps= 115,
    chol= 183,
    thalach=171
)

testheart10 = OrmHeart(
    heart_id= 10,
    age= 55,
    sex= 'female',
    trestbps= 115,
    chol= 183,
    thalach=167
)
db.session.add_all([
    Lesha,
    Vlad,
    Dima,
    Ivan,
    Jenya,
    Nastya,
    Max,
    Serg,
    Kate,
    URTI,
    URTI2,
    Flu,
    Flu2,
    Migraine,
    High_pressure,
    Cold,
    Cold2,
    Croup,
    Croup2,
    cough,
    Pertussis,
    throat,
    head,
    testheart,
    testheart2,
    testheart3,
    testheart4,
    testheart5,
    testheart6,
    testheart7,
    testheart8,
    testheart9,
    testheart10
])

db.session.commit()


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/patients')
def patients():
    res = db.session.query(OrmPatient).all()

    return render_template('patients_table.html', patients=res)

@app.route('/create_patient', methods=['POST', 'GET'])
def create_patient():
    form = PatientForm()

    next_id_prep = max(db.session.query(OrmPatient.patient_id).all())
    next_id = next_id_prep[0] + 1

    if request.method == 'POST':
        if form.validate():
            try:
                new_patient = OrmPatient(
                    patient_id=next_id,
                    patient_age=form.patient_age.data,
                    patient_height=form.patient_height.data,
                    patient_weight=form.patient_weight.data,
                    patient_temperature=form.patient_temperature.data
                )
                db.session.add(new_patient)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('patient_form.html', form=form)
        else:
            return render_template('patient_form.html', form=form)
    elif request.method == 'GET':
        return render_template('patient_form.html', form=form)


@app.route('/patient_edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    form = PatientForm()
    result = db.session.query(OrmPatient).filter(OrmPatient.patient_id == id).one()

    if request.method == 'GET':


        form.patient_age.data = result.patient_age
        form.patient_height.data = result.patient_height
        form.patient_weight.data = result.patient_weight
        form.patient_temperature.data = result.patient_temperature

        return render_template('edit_patient.html', form=form, form_name='edit patient')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.patient_age = form.patient_age.data
                result.patient_height = form.patient_height.data
                result.patient_weight = form.patient_weight.data
                result.patient_temperature = form.patient_temperature.data

                db.session.commit()
                return redirect('/patients')
            except:
                return render_template('edit_patient.html', form=form)
        else:
            return render_template('edit_patient.html', form=form)

@app.route('/delete_patient/<string:id>', methods=['GET', 'POST'])
def delete_patient(id):
    result = db.session.query(OrmPatient).filter(OrmPatient.patient_id == id).one()
    symptoms_rows = db.session.query(OrmSymptom).filter(OrmSymptom.patient_id == id).all()
    symptom_ids = db.session.query(OrmSymptom.symptom_id).filter(OrmSymptom.patient_id == id).all()

    symp_ids = []
    for id  in symptom_ids:
        symp_ids.append(id[0])

    for id in symp_ids:
        dises = db.session.query(OrmDisease).filter(OrmDisease.symptom_id == id).all()
        for row in dises:
            db.session.delete(row)

    for row in symptoms_rows:
        db.session.delete(row)

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')

# SYMPTOM
@app.route('/symptoms')
def symptoms():
    res = db.session.query(OrmSymptom).all()

    return render_template('symptoms_table.html', symptoms=res)

@app.route('/new_symptom/<int:id>', methods=['GET', 'POST'])
def new_symptom(id):
    form = SymptomForm()

    u_id_prep = db.session.query(OrmPatient.patient_id).filter(OrmPatient.patient_id == id).one()
    u_id = u_id_prep[0]
    next_id_prep = max(db.session.query(OrmSymptom.symptom_id).all())
    next_id = next_id_prep[0] + 1

    if request.method == 'POST':
        if form.validate():
            try:
                new_symptom = OrmSymptom(
                    symptom_id=next_id,
                    description=form.description.data,
                    patient_id=u_id
                )
                db.session.add(new_symptom)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('symptom_form.html', form=form)
        else:
            return render_template('symptom_form.html', form=form)
    elif request.method == 'GET':
        return render_template('symptom_form.html', form=form)

@app.route('/edit_symptom/<int:id>', methods=['GET', 'POST'])
def edit_symptom(id):
    form = EditSymptomForm()
    result = db.session.query(OrmSymptom).filter(OrmSymptom.symptom_id == id).one()

    if request.method == 'GET':

        form.description.data = result.description

        return render_template('edit_symptom.html', form=form, form_name='edit symptom')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.description = form.description.data
                db.session.commit()
                return redirect('/symptoms')
            except:
                return render_template('edit_symptom.html', form=form)
        else:
            return render_template('edit_symptom.html', form=form)


@app.route('/delete_symptom/<int:id>', methods=['GET', 'POST'])
def delete_symptom(id):
    result = db.session.query(OrmSymptom).filter(OrmSymptom.symptom_id == id).one()
    diseases_rows = db.session.query(OrmDisease).filter(OrmDisease.symptom_id == id).all()

    for row in diseases_rows:
        db.session.delete(row)

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')


# DISEASE
@app.route('/diseases')
def diseases():
    res = db.session.query(OrmDisease).all()

    return render_template('diseases_table.html', diseases=res)


@app.route('/new_disease/<int:id>', methods=['GET', 'POST'])
def new_disease(id):
    form = DiseaseForm()

    s_id_prep = db.session.query(OrmSymptom.symptom_id).filter(OrmSymptom.symptom_id == id).one()
    s_id = s_id_prep[0]
    next_id_prep = max(db.session.query(OrmDisease.disease_id).all())
    next_id = next_id_prep[0] + 1

    if request.method == 'POST':
        if form.validate():
            try:
                new_disease = OrmDisease(
                    disease_id=next_id,
                    disease_name=form.disease_name.data,
                    severity=form.severity.data,
                    symptom_id=s_id
                )
                db.session.add(new_disease)
                db.session.commit()
                return render_template('success.html')
            except:
                return render_template('disease_form.html', form=form)
        else:
            return render_template('disease_form.html', form=form)
    elif request.method == 'GET':
        return render_template('disease_form.html', form=form)


@app.route('/edit_disease/<string:id>', methods=['GET', 'POST'])
def edit_disease(id):
    form = EditDiseaseForm()
    result = db.session.query(OrmDisease).filter(OrmDisease.disease_id == id).one()

    if request.method == 'GET':

        form.disease_name.data = result.disease_name
        form.severity.data = result.severity

        return render_template('edit_disease.html', form=form, form_name='edit disease')
    elif request.method == 'POST':
        if form.validate():
            try:
                result.disease_name = form.disease_name.data
                result.severity = form.severity.data
                db.session.commit()
                return redirect('/diseases')
            except:
                return render_template('edit_disease.html', form=form)
        else:
            return render_template('edit_disease.html', form=form)



@app.route('/delete_disease/<string:id>', methods=['GET', 'POST'])
def delete_disease(id):
    result = db.session.query(OrmDisease).filter(OrmDisease.disease_id == id).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('success.html')

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    my_query = (
        db.session.query(
            OrmPatient.patient_id,
            func.count(OrmSymptom.symptom_id).label('symptom_count')
        ).join(OrmSymptom, OrmSymptom.patient_id == OrmPatient.patient_id).
            group_by(OrmPatient.patient_id)
    ).all()

    dy_query = (
        db.session.query(
            OrmSymptom.symptom_id,
            func.count(OrmDisease.disease_id).label('disease_count')
        ).join(OrmDisease, OrmDisease.symptom_id == OrmSymptom.symptom_id).
            group_by(OrmSymptom.symptom_id)
    ).all()

    cor_query = (
        db.session.query(
            OrmHeart.age, OrmHeart.trestbps
        ).all()
    )

    patient_id, symptom_count = zip(*my_query)

    bar = go.Bar(
        x=patient_id,
        y=symptom_count
    )

    description, disease_count = zip(*dy_query)
    pie = go.Pie(
        labels=description,
        values=disease_count
    )

    age, trestbps = zip(*cor_query)

    trace = go.Scatter(
        x=age,
        y=trestbps,
        mode='markers'
    )

    data = {
        "bar": [bar],
        "pie": [pie],
        "trace": [trace]
    }
    graphs_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    corr_m = np.corrcoef(age, trestbps)

    return render_template('dashboard.html', graphsJSON=graphs_json,corr_m =corr_m[0][1] )



@app.route('/heart')
def hearts():
    res = db.session.query(OrmHeart).all()

    return render_template('heart_table.html', hearts=res)

@app.route('/create_heart', methods=['POST', 'GET'])
def create_heart():

    form = HeartForm()
    if request.method == 'POST':
        if form.validate():
            new_patient = OrmHeart(
                heart_id=form.heart_id.data,
                age=form.age.data,
                sex=form.sex.data,
                trestbps=form.trestbps.data,
                chol=form.chol.data,
                thalach=form.thalach.data
            )
            db.session.add(new_patient)
            db.session.commit()
            return render_template('success.html')
        else:
            return render_template('heart_form.html', form=form)
    elif request.method == 'GET':
        return render_template('heart_form.html', form=form)




@app.route('/heartdiagnostics/<string:heart_id>', methods=['POST', 'GET'])
def diagnostic(heart_id):
    result_prep = db.session.query(OrmHeart.age, OrmHeart.sex, OrmHeart.trestbps, OrmHeart.chol, OrmHeart.thalach).filter(OrmHeart.heart_id == heart_id).one()
    result = list(result_prep)

    if result[1] == 'male':
        result[1] = 1
    else:
        result[1] = 0

    df = pd.read_csv('heart.csv')

    x_matrix_prep = df.drop(columns=['target', 'cp', 'restecg', 'slope', 'ca', 'thal', 'fbs', 'exang', 'oldpeak', ])

    x_matrix = x_matrix_prep.to_numpy()
    y_vector = df.target.to_numpy()

    logistic = LogisticRegression(max_iter=10000)
    logistic.fit(x_matrix, y_vector)
    prob = logistic.predict_proba([result])[0][1]
    prob_proc = round(prob * 100, 2)
    conclusion = ''
    if prob < 0.35:
        conclusion = 'Серьезной угрозы нет'
    if prob >= 0.35 and prob < 0.7:
        conclusion = 'Вам нужно обследоваться'
    if prob >= 0.7:
        conclusion = 'Срочно обратитесь к врачу!'

    model = KMeans(n_clusters=3)
    model.fit(x_matrix_prep)
    predict = model.predict([result])

    return render_template('heart_conclusion.html', prob= prob_proc, conclusion = conclusion,predict = predict)


@app.route('/show_disease/<string:id>')
def show_disease(id):

    res = db.session.query(
        OrmSymptom.description,OrmDisease.disease_id, OrmDisease.disease_name
    ).join(OrmDisease, OrmDisease.symptom_id == OrmSymptom.symptom_id).filter(OrmSymptom.symptom_id == id).all()

    return render_template('disease_for_symptom.html', diseases=res)




if __name__ == '__main__':
    app.debug = True
    app.run()

