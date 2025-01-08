
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
