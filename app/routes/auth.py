from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.administrador import Administrador
from app.models.aprendiz import Aprendices
from app.models.usuario import Usuarios
from flask import Flask,render_template,request,redirect,url_for,flash
from app import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
def index():
    return render_template('principal/index.html')


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Procesar el formulario de registro
        nombre = request.form['nombre']
        documento = request.form['documento']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        password = request.form['password']
        tipo    = request.form['tipo']

        nuevo_usuario = Usuarios(nombre=nombre, documento=documento, direccion=direccion,telefono=telefono, correo=correo, password=password, tipo=tipo)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Registro exitoso!', 'success')
            return render_template('principal/index.html')
        except:
            flash('Error en el registro. Por favor, intente de nuevo.', 'danger')
    return render_template('registro.html')




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo= request.form['correo']
        password = request.form['password']

       # busca el administrador con las credenciales proporcionadas
        administrador = Administrador.query.filter_by(correoAdministrador=correo, passwordAdministrador =password).first()
        
        if administrador:
            login_user(administrador)
            flash("Login successful!", "success")

            return redirect(url_for('auth.dashboard'))
        
        aprendiz = Aprendices.query.filter_by(correoAprendiz=correo, passwordAprendiz=password).first()
        
        if aprendiz:
            login_user(aprendiz)
            flash("Login successful!", "success")

            return render_template("auth.dashboar")
        
        flash('Invalid credentials. Please try again.', 'danger')
    
        

    
    return render_template("login/login.html")
    


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return f'Welcome, {current_user.usuario}! This is your dashboard.'

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))







