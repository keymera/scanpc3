from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import socket
import re, uuid
import os
import subprocess
import psutil
import string
import os.path
import shutil
import platform
from datetime import date
from datetime import datetime

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scanpc'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/test', methods =['POST', 'GET'])
def test():
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT area FROM scan')
    data = cur.fetchall()
    cur.close()

    return render_template('botones_areas.html', contacts = data)


@app.route('/')
def Index():
    return render_template('home.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        #obtencion del nombre
        hostname = socket.gethostname()
        #obtencion de la IP
        addr = socket.gethostbyname(hostname)
        sistema = platform.system()
        version = platform.release()
        os = (sistema + " " + str(version))
        name = request.form['name']
        user = request.form['user']
        area = request.form['area']
        correo = request.form['correo']
        fecha_registro = date.today()
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO scan (name, user, correo, area, addr,os, hostname, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (name, user, correo, area,addr,os, hostname, fecha_registro))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Inventario'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM scan WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST': 
        #obtencion del nombre
        hostname = socket.gethostname()
        #obtencion de la IP
        addr = socket.gethostbyname(hostname)
        sistema = platform.system()
        version = platform.release()
        os = (sistema + " " + str(version))
        name = request.form['name']
        user = request.form['user']
        area = request.form['area']
        correo = request.form['correo']
        fecha_registro = date.today()
        os = request.form['os']
        cur = mysql.connection.cursor()
        
        cur.execute("""
            UPDATE scan
            SET name = %s,
                user = %s,
                correo = %s,
                area = %s,
                addr = %s,
                os = %s,
                hostname = %s,
                fecha_registro = %s
            WHERE id = %s
        """, (name, user, correo, area,addr,os, hostname, fecha_registro, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Inventario'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM scan WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Inventario'))

@app.route('/inventario')
def Inventario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM scan')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/Busqueda')
def Busqueda():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM scan')
    data = cur.fetchall()
    cur.close()
    return render_template('Busqueda.html', contacts = data)

@app.route('/about')
def About():
    return render_template ('about.html')

@app.route('/resumen', methods = ['POST','GET'])
def Cuadro():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(id), area FROM scan GROUP BY area')
    data = cur.fetchall()
    cur.close()

    return render_template ('resumenporarea1.html', contacts = data)

@app.route('/Grupos')
def Grupos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM grupos')
    data = cur.fetchall()
    cur.close()
    return render_template('crud_grupos.html', contacts = data)

@app.route('/add_grupo', methods=['POST'])
def add_grupos():
    if request.method == 'POST':
        grupo = request.form['grupo']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO grupos (grupo, descripcion) VALUES (%s,%s)", (grupo, descripcion))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Grupos'))

@app.route('/edit_grupos/<id>', methods = ['POST', 'GET'])
def get_grupos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM grupos WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_grupo.html', contact = data[0])

@app.route('/update_grupos/<id>', methods=['POST'])
def update_grupos(id):
    if request.method == 'POST':
        grupo = request.form['grupo']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE grupos
            SET grupo = %s,
                descripcion = %s,
            WHERE id = %s
        """, (grupo, descripcion, id))
        flash('grupo Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Grupos'))

@app.route('/delete_grupos/<string:id>', methods = ['POST','GET'])
def delete_grupos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM grupos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('grupo Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=4000, debug=True)
