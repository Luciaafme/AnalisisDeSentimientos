import sqlite3
from textblob import TextBlob

# Ruta de la nueva base de datos
nueva_db_path = 'C:/Users/lucia/PycharmProjects/pythonProject/database/opiniones.db'

# Conectar a la nueva base de datos
nueva_conn = sqlite3.connect(nueva_db_path)

# Crear un cursor para ejecutar consultas en la nueva base de datos
nueva_cursor = nueva_conn.cursor()

# Reemplazar 'nombre_de_tabla' con el nombre que desees para tu tabla en la nueva base de datos
nueva_table_name = 'Opiniones'

# Crear la tabla en la nueva base de datos si no existe
create_table_query = f'''
CREATE TABLE IF NOT EXISTS {nueva_table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel TEXT,
    opinion TEXT,
    polaridad REAL,
    subjetividad REAL,
    sentimiento TEXT
);
'''
nueva_cursor.execute(create_table_query)

# Guardar los cambios en la nueva base de datos
nueva_conn.commit()

# Conectar a la base de datos original
db_path = 'C:/Users/lucia/PycharmProjects/pythonProject/database/TripadvisorDatos.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Reemplaza 'nombre_de_tabla' con el nombre de tu tabla original
table_name = 'DatosDeReseñasTripadvisor'

# Consulta SQL para seleccionar todos los datos de la tabla original
query = f"SELECT resena, hotel FROM {table_name}"
cursor.execute(query)
results = cursor.fetchall()

# Insertar datos en la nueva base de datos
for result in results:
    opinion, hotel = result
    blob1 = TextBlob(str(opinion))
    polaridad = blob1.sentiment.polarity  # Obtener la polaridad del sentimiento
    subjetividad = blob1.sentiment.subjectivity
    sentimiento = 'Positiva' if polaridad > 0 else 'Negativa' if polaridad < 0 else 'Neutral'
    insert_query = f"INSERT INTO {nueva_table_name} (hotel, opinion, polaridad, subjetividad, sentimiento) VALUES (?, ?, ?, ?, ?)"
    nueva_cursor.execute(insert_query, (str(hotel),str(opinion), polaridad, subjetividad, sentimiento))

# Guardar los cambios en la nueva base de datos
nueva_conn.commit()

# Cerrar cursores y conexiones
cursor.close()
conn.close()
nueva_cursor.close()
nueva_conn.close()

