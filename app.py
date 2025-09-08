from flask import Flask, render_template, request
import json, csv, os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configuración de SQLite
Base = declarative_base()
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String)

db_path = os.path.join(os.path.dirname(__file__), 'database/usuarios.db')
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    nombre = request.form['nombre']
    correo = request.form['correo']

    # Guardar en TXT
    with open('datos/datos.txt', 'a') as f:
        f.write(f'{nombre},{correo}\n')

    # Guardar en JSON
    try:
        with open('datos/datos.json', 'r') as f:
            data = json.load(f)
    except:
        data = []
    data.append({'nombre': nombre, 'correo': correo})
    with open('datos/datos.json', 'w') as f:
        json.dump(data, f)

    # Guardar en CSV
    with open('datos/datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, correo])

    # Guardar en SQLite
    nuevo_usuario = Usuario(nombre=nombre, correo=correo)
    session.add(nuevo_usuario)
    session.commit()

    return render_template('resultado.html', nombre=nombre, correo=correo)

if __name__ == '__main__':
    app.run(debug=True)
