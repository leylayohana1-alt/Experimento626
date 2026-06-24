from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dulceeden123"

# --- DATOS DE ACCESO DEL ADMINISTRADOR ---
USUARIO_ADMIN = "lale"
CLAVE_ADMIN = "balucopito20"

# Diccionario de productos con IDs únicos
productos_data = {
    "pasteles":[
        {
            "id": 1,
            "nombre":"Pastel de Chocolate",
            "precio":60,
            "stock": 25,
            "imagen":"https://www.cocinadelirante.com/800x600/filters:format(webp):quality(75)/sites/default/files/images/2023/08/receta-de-pastel-de-chocolate-facil.jpg"
        },
        {
            "id": 2,
            "nombre":"Pastel de Fresa",
            "precio":50,
            "stock": 25,
            "imagen":"https://www.elle-et-vire.com/uploads/cache/930w/uploads/recip/recipe/3779/6377ad3abb209_bra004354-iconic-strawberry-ca.jpg"
        },
        {
            "id": 3,
            "nombre":"Pastel de Cumpleaños",
            "precio":50,
            "stock": 25,
            "imagen":"https://yanubapasteleria.com/wp-content/uploads/2022/01/Nuevo-proyecto-23.jpg"
        },
        {
            "id": 4,
            "nombre":"Pastel de Cumpleaños",
            "precio":100,
            "stock": 25,
            "imagen":"https://wiltonenespanol.com/wp-content/uploads/2020/11/Sprinkle-on-the-Fun-Birthday-Cake.jpg"
        },
        {
            "id": 5,
            "nombre":"Pastel de Cumpleaños",
            "precio":300,
            "stock": 25,
            "imagen":"https://www.marialunarillos.com/blog/wp-content/uploads/2023/01/receta-tarta-infantil-cumpleanos-animalitos-0.jpg"
        },
        {
            "id": 6,
            "nombre":"Pastel de Boda",
            "precio":700,
            "stock": 25,
            "imagen":"https://images.unsplash.com/photo-1623428454614-abaf00244e52?q=80&w=387&auto=format&fit=crop"
        },
        {
            "id": 7,
            "nombre":"Pastel de Boda",
            "precio":500,
            "stock": 25,
            "imagen":"https://plus.unsplash.com/premium_photo-1675720060105-ba50ca9e21a7?q=80&w=871&auto=format&fit=crop"
        },
        {
            "id": 8,
            "nombre":"Pastel de Boda",
            "precio":700,
            "stock": 25,
            "imagen":"https://images.unsplash.com/photo-1519654793190-2e8a4806f1f2?q=80&w=387&auto=format&fit=crop"
        }
    ],
    "bebidas":[
        {
            "id": 9,
            "nombre":"Café Latte",
            "precio":10,
            "stock": 10,
            "imagen":"https://www.cuisinart.com/dw/image/v2/ABAF_PRD/on/demandware.static/-/Sites-us-cuisinart-sfra-Library/default/dw42dcae51/images/recipe-Images/cafe-latte1-recipe_resized.jpg"
        },
        {
            "id": 10,
            "nombre":"Capuccino",
            "precio":12,
            "stock": 10,
            "imagen":"https://www.cabucoffee.com/newimages/Guia-Cappuccino.jpg"
        }
    ],
    "panes_dulces":[
        {
            "id": 11,
            "nombre":"trufas",
            "precio":10,
            "stock": 30,
            "imagen":"https://dulcesperu.com/wp-content/uploads/2025/12/trufas-navidad-1.jpg"
        },
        {
            "id": 12,
            "nombre":"muffins",
            "precio":12,
            "stock": 20,
            "imagen":"https://cdn.vegkit.com/wp-content/uploads/sites/2/2024/02/18160130/berry_muffins_1.jpg"
        },
        {
            "id": 13,
            "nombre":"pan de masa madre",
            "precio":12,
            "stock": 5,
            "imagen":"https://veggiefestchicago.org/wp-content/uploads/2025/01/AdobeStock_968234066.jpg"
        }
    ]
}

proximo_id = 14


# --- RUTAS DE NAVEGACIÓN Y MENÚ ---

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/pasteles")
def pasteles():
    return render_template("pasteles.html", productos=productos_data["pasteles"])

@app.route("/bebidas")
def bebidas():
    return render_template("bebidas.html", productos=productos_data["bebidas"])

@app.route("/panes_dulces")
def panes_dulces():
    return render_template("panes_dulces.html", productos=productos_data["panes_dulces"])

@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        with open("registros.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre},{correo},{telefono}\n")
        mensaje = "Registro guardado correctamente"
    return render_template("registro.html", mensaje=mensaje)


# --- RUTAS DEL CARRITO ---

@app.route("/carrito")
def carrito():
    carrito = session.get("carrito", [])
    total = sum(float(producto["precio"]) for producto in carrito)
    return render_template("carrito.html", carrito=carrito, total=total)

@app.route("/agregar")
def agregar():
    nombre = request.args.get("nombre")
    precio = float(request.args.get("precio"))
    
    carrito = session.get("carrito", [])
    carrito.append({
        "nombre": nombre,
        "precio": precio
    })
    session["carrito"] = carrito
    
    return redirect(request.referrer)

@app.route("/eliminar/<int:indice>")
def eliminar(indice):
    carrito = session.get("carrito", [])
    if 0 <= indice < len(carrito):
        carrito.pop(indice)
    session["carrito"] = carrito
    return redirect(request.referrer)

@app.route("/vaciar")
def vaciar():
    session["carrito"] = []
    return redirect(request.referrer)


# --- RUTAS DE PAGO ---

@app.route("/pago_bcp")
def pago_bcp():
    carrito = session.get("carrito", [])
    total = sum(float(producto["precio"]) for producto in carrito)
    return render_template("pago_bcp.html", total=total)

@app.route("/procesar_pago", methods=["POST"])
def procesar_pago():
    carrito = session.get("carrito", [])
    if carrito:
        with open("ventas.txt", "a", encoding="utf-8") as archivo:
            for producto in carrito:
                archivo.write(f"{producto['nombre']},{producto['precio']}\n")
                
    session["carrito"] = []
    return """
    <h1>✅ Pago realizado con éxito</h1>
    <h2>Gracias por comprar en Dulce Edén 🍰</h2>
    <a href="/">Volver al inicio</a>
    """


# --- 🔐 SECCIÓN SEGURIDAD LOGIN ---

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        
        if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
            session["admin_logueado"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"
            
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("admin_logueado", None)
    return redirect(url_for("login"))


# --- 📊 SECCIÓN DASHBOARD & CRUD (PROTEGIDO) ---

@app.route("/admin")
def admin_dashboard():
    if not session.get("admin_logueado"):
        return redirect(url_for("login"))
        
    return render_template("admin.html", productos=productos_data)

@app.route("/admin/crear", methods=["POST"])
def admin_crear():
    if not session.get("admin_logueado"):
        return redirect(url_for("login"))
        
    global proximo_id
    categoria = request.form["categoria"]
    nuevo_producto = {
        "id": proximo_id,
        "nombre": request.form["nombre"],
        "precio": float(request.form["precio"]),
        "imagen": request.form["imagen"]
    }
    productos_data[categoria].append(nuevo_producto)
    proximo_id += 1
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/eliminar/<categoria>/<int:prod_id>")
def admin_eliminar(categoria, prod_id):
    if not session.get("admin_logueado"):
        return redirect(url_for("login"))
        
    if categoria in productos_data:
        productos_data[categoria] = [p for p in productos_data[categoria] if p["id"] != prod_id]
    return redirect(url_for("admin_dashboard"))


# --- CONTROL DE INVENTARIO AUTOMÁTICO CORREGIDO ---
@app.route("/admin/dashboard")
def dashboard():
    if not session.get("admin_logueado"):
        return redirect(url_for("login"))

    # 1. Leer las ventas guardadas en ventas.txt
    ventas = []
    try:
        with open("ventas.txt", "r", encoding="utf-8") as archivo:
            ventas = archivo.readlines()
    except:
        ventas = []

    # Procesamos las cantidades vendidas por cada nombre y sumamos ingresos
    dict_ventas = {}
    total_unidades_vendidas = 0
    total_ingresos = 0.0

    for venta in ventas:
        if "," in venta:
            nombre, precio = venta.strip().split(",")
            dict_ventas[nombre] = dict_ventas.get(nombre, 0) + 1
            total_unidades_vendidas += 1
            total_ingresos += float(precio)

    # 2. Calcular el Stock Disponible (Inicial - Vendidos)
    inventario_control = []
    total_stock_actual_disponible = 0
    total_productos_catalogo = 0

    for categoria, lista_prods in productos_data.items():
        for prod in lista_prods:
            nombre = prod["nombre"]
            stock_inicial = prod.get("stock", 10) 
            total_productos_catalogo += stock_inicial
            
            unidades_vendidas = dict_ventas.get(nombre, 0)
            
            # Operación: Sobran = Inicial - Vendidos
            stock_restante = stock_inicial - unidades_vendidas
            if stock_restante < 0:
                stock_restante = 0
                
            total_stock_actual_disponible += stock_restante

            inventario_control.append({
                "nombre": nombre,
                "inicial": stock_inicial,
                "vendidos": unidades_vendidas,
                "restante": stock_restante
            })

    # ENVIAMOS LAS VARIABLES CORRECTAS A CADA CASILLA
    return render_template(
        "dashboard.html",
        total_productos=total_productos_catalogo,        # Tarjeta Azul
        total_vendidos=total_unidades_vendidas,         # Tarjeta Verde
        stock_restante=total_stock_actual_disponible,   # Tarjeta Amarilla (Ahora sí dirá cuántos sobran)
        ingresos=total_ingresos,                        # Tarjeta Celeste (Ahora sí tendrá el dinero: 1094.0)
        productos=dict_ventas,                          # Gráfica
        inventario=inventario_control                   # Tabla de abajo
    )

if __name__ == "__main__":
    app.run(debug=True)