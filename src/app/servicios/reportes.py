import pandas as pd
from datetime import datetime

def generar_reporte_excel(envios, nombre_archivo=None):
    if nombre_archivo is None:
        fecha = datetime.now().strftime("%Y%m%d_%H%M")
        nombre_archivo = f"reporte_envios_{fecha}.xlsx"

    # Convertir objetos Envio a diccionarios
    datos = [envio.a_dicc() for envio in envios]

    # Crear DataFrame o encuadramiento de datos.
    df = pd.DataFrame(datos)

    # Crear Excel con formato
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Envíos', index=False)

        # Formato a la hoja
        worksheet = writer.sheets['Envíos']

        # Autoajustar columnas
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    return nombre_archivo