import sqlite3

from flair.models import TextClassifier
from flair.data import Sentence

# Modelo preentrenado para análisis de sentimientos en español
sentiment_model_es = TextClassifier.load('sentiment-fast')

# Conectar a la base de datos
db_path = 'C:/Users/lucia/PycharmProjects/pythonProject/database/TripadvisorDatos.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Reemplazar 'nombre_de_tabla' con el nombre de tu tabla en la base de datos
table_name = 'DatosDeReseñasTripadvisor'

# Consulta SQL para seleccionar todas las opiniones de la tabla
query = f"SELECT resena FROM {table_name}"
cursor.execute(query)
opiniones = cursor.fetchall()

# Conectar a la nueva base de datos para almacenar resultados
nueva_db_path = 'C:/Users/lucia/PycharmProjects/pythonProject/database/opiniones.db'
nueva_conn = sqlite3.connect(nueva_db_path)
nueva_cursor = nueva_conn.cursor()

# Crear la tabla en la nueva base de datos si no existe
create_table_query = '''
CREATE TABLE IF NOT EXISTS OpinionesAnalizadasFlair (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opinion TEXT,
    sentimiento TEXT
);
'''
nueva_cursor.execute(create_table_query)
nueva_conn.commit()

# Realizar análisis de sentimientos y almacenar resultados en la nueva base de datos
for opinion in opiniones:
    sentence = Sentence(str(opinion))
    sentiment_model_es.predict(sentence)
    sentimiento = sentence.labels[0].value

    insert_query = '''
    INSERT INTO OpinionesAnalizadasFlair (opinion, sentimiento) VALUES (?, ?)
    '''
    nueva_cursor.execute(insert_query, (str(opinion), sentimiento))
    nueva_conn.commit()

# Cerrar conexiones
cursor.close()
conn.close()
nueva_cursor.close()
nueva_conn.close()

