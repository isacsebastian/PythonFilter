# __init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config['UPLOAD_FOLDER'] = 'data/uploaded_files'
    app.config['PROCESSED_FOLDER'] = 'data/processed'
    app.secret_key = 'your_secret_key'

    # Registrar rutas
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

# routes.py
from flask import Blueprint, request, render_template, jsonify, send_file
from .filters import apply_filters
from .utils import generate_pdf, generate_csv
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title="Filtrado de Datos")

@main_bp.route('/filter', methods=['POST'])
def filter_data():
    # Obtener parámetros del formulario
    cliente_id = request.form.get('cliente_id')
    vendedor_id = request.form.get('vendedor_id')
    categoria = request.form.get('categoria')
    mes = request.form.get('mes')

    try:
        # Aplicar filtros a los datos
        filtered_data = apply_filters(cliente_id, vendedor_id, categoria, mes)
        return render_template('results.html', title="Resultados", data=filtered_data)
    except Exception as e:
        return render_template('error.html', title="Error", message=str(e))

@main_bp.route('/export', methods=['POST'])
def export_data():
    export_type = request.form.get('type')
    filtered_data = request.form.get('data')  # Datos ya filtrados

    try:
        if export_type == 'pdf':
            file_path = generate_pdf(filtered_data)
        else:
            file_path = generate_csv(filtered_data)

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# models.py
class Client:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Product:
    def __init__(self, category, subcategory, material, description):
        self.category = category
        self.subcategory = subcategory
        self.material = material
        self.description = description

# filters.py
import pandas as pd

def apply_filters(cliente_id, vendedor_id, categoria, mes):
    # Cargar datos desde el CSV
    file_path = 'data/Base.csv'
    df = pd.read_csv(file_path)

    # Filtrar por cliente y vendedor
    if cliente_id:
        df = df[df['Cliente'] == int(cliente_id)]
    if vendedor_id:
        df = df[df['Vendedor'] == int(vendedor_id)]

    # Filtrar por categoría
    if categoria:
        df = df[df['Categoria'] == categoria]

    # Filtrar por mes
    if mes:
        df = df[df[mes].notnull()]

    return df.to_dict(orient='records')

# utils.py
from fpdf import FPDF
import pandas as pd
import os

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte Filtrado", ln=True, align='C')

    for row in data:
        pdf.cell(200, 10, txt=str(row), ln=True, align='L')

    file_path = os.path.join('data/processed', 'filtered_data.pdf')
    pdf.output(file_path)
    return file_path

def generate_csv(data):
    file_path = os.path.join('data/processed', 'filtered_data.csv')
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return file_path
