##################################################################################################################################
#
# Lee un fichero .csv con campos separados por |, lo guarda en un dataframe, y lo mete en mi lista de lectura multimedia en Notion
# Info sobre el api de Notion para esto:
# https://www.youtube.com/watch?v=M1gu9MDucMA
# https://www.python-engineer.com/posts/notion-api-python/
#
##################################################################################################################################

import pandas as pd
import requests
import json

def create_page(data: dict, target_database: str, headers):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": target_database}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

# Leer la configuración
with open('notion_secrets.json', 'r') as file:
    my_notion_config = json.load(file)

my_database = my_notion_config["database_id"]

my_headers = {
    "Authorization": "Bearer " + my_notion_config["token"],
    "Content-Type": my_notion_config["Content-Type"],
    "Notion-Version": my_notion_config["Notion-Version"]
}

# Leer .csv y pasar a dataframe
fichero_ver_mas_tarde = "data.csv"
df = pd.read_csv(fichero_ver_mas_tarde, sep="|")
print(df)

# Pasar a dataframe

# conectarse a notion
# url = ""
# my_url = f"https://api.notion.com/v1/databases/{my_database}/query"

# print(my_url)

# response = requests.post(url = my_url, headers = my_headers)
# print(response.status_code)

# my_database_info = json.loads(response.content)
# print(my_database_info)




# Escribir en la BD
"""
pages = get_pages()

for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    published = datetime.fromisoformat(published)
"""


for index, row in df.iterrows():
    titulo = row.loc['VIDEO TITLE']
    enlace = row.loc['VIDEO LINK']
    duracion = row.loc['VIDEO DURATION']
    canal = row.loc['CHANNEL']

    my_data = {"Título": {"id": "title","type": "title", "title": [ {"type": "text","text": {"content": titulo} }]},
            "enlace": {"id": "eHgM","type": "url","url": enlace},
            "duracion": {"id": "nEws","type": "rich_text","rich_text": [{"type": "text", "text": {"content": duracion}}]},
            "canal": {"id": "%3BAC%3A","type": "rich_text","rich_text": [{"type": "text", "text": {"content": canal}}]},
            "leido": {"id": "%3Cd%3CP","type": "checkbox", "checkbox": False}
            # "etiquetas": {"id": "%3B~iS","type": "multi_select","multi_select": [{"name": "BBBBBB"},{"name": "MI NUEVA EtiQuetA"}]}
            }
    
    create_page(my_data, my_database, my_headers)

# TO DO:
# Leer las etiquetas del csv y el dataframe y meterlas correctamente 
# Traducir marca de leido a true false
# Refactorizar para mejorar modularidad del código

# {"enlace": {"id": "eHgM","type": "url","url": "http://youtu.be/kfdskfj"}}
