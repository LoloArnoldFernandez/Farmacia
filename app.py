from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

bootstrap=Bootstrap(app)  

# Función para obtener todos los clientes desde la base de datos
def obtener_clientes():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# Función para obtener todos los productos desde la base de datos
def obtener_productos():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para obtener todas las facturas desde la base de datos
def obtener_facturas():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas')
    facturas = cursor.fetchall()
    conn.close()
    return facturas

# Función para guardar un cliente en la base de datos
def guardar_cliente(nombre, direccion, telefono, correo):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nombre, direccion, telefono, correo) VALUES (?, ?, ?, ?)',
                   (nombre, direccion, telefono, correo))
    conn.commit()
    conn.close()

# Función para buscar clientes en la base de datos
def buscar_clientes(busqueda):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE nombre LIKE ?', ('%' + busqueda + '%',))
    clientes = cursor.fetchall()
    conn.close()
    return clientes
def obtener_productos():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

# Función para guardar un producto en la base de datos
def guardar_producto(nombre, precio, stock):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)',
                   (nombre, precio, stock))
    conn.commit()
    conn.close()

# Función para obtener las facturas desde la base de datos
def obtener_facturas():
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas')
    facturas = cursor.fetchall()
    conn.close()
    return facturas

# Función para guardar una factura en la base de datos
def guardar_factura(cliente_id, sucursal, fecha, total):
    conn = sqlite3.connect('farmacia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO facturas (cliente_id, sucursal, fecha, total) VALUES (?, ?, ?, ?)',
                   (cliente_id, sucursal, fecha, total))
    conn.commit()
    conn.close()
# Ruta de la página de inicio
@app.route('/')
def index():
    return render_template('index.html', active='inicio')

# Ruta de la página de clientes
@app.route('/clientes')
def clientes():
    clientes = obtener_clientes()  # Función para obtener los clientes desde la base de datos
    return render_template('clientes.html', active='clientes', clientes=clientes)
# Ruta para agregar un cliente
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        guardar_cliente(nombre, direccion, telefono, correo)  # Función para guardar el cliente en la base de datos
        return redirect('/clientes')
    return render_template('agregar_cliente.html')

# Ruta para buscar clientes
@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    busqueda = request.form['busqueda']
    clientes = buscar_clientes(busqueda)  # Función para buscar clientes en la base de datos
    return render_template('clientes.html', active='clientes', clientes=clientes)

# Ruta de la página de productos
@app.route('/productos')
def productos():
    productos = obtener_productos()  # Función para obtener los productos desde la base de datos
    return render_template('productos.html', active='productos', productos=productos)

# Ruta para agregar un producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        guardar_producto(nombre, precio, stock)  # Función para guardar el producto en la base de datos
        return redirect('/productos')
    return render_template('agregar_producto.html', productos=productos)


# Ruta de la página de facturas
@app.route('/facturas')
def facturas():
    facturas = obtener_facturas()  # Función para obtener las facturas desde la base de datos
    return render_template('facturas.html', active='facturas', facturas=facturas)
# Ruta para agregar una factura
@app.route('/agregar_factura', methods=['GET', 'POST'])
def agregar_factura():
    if request.method == 'POST':
        cliente_id = int(request.form['cliente_id'])
        sucursal = request.form['sucursal']
        fecha = request.form['fecha']
        total = float(request.form['total'])
        guardar_factura(cliente_id, sucursal, fecha, total)  # Función para guardar la factura en la base de datos
        return redirect('/facturas')
    clientes = obtener_clientes()  # Función para obtener los clientes desde la base de datos
    return render_template('agregar_factura.html', facturas=facturas)

if __name__ == '__main__':
    app.run()
