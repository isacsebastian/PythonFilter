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