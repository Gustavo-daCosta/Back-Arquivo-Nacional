from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from LLM.AI import ask_to_ai
from extractors.jpg_extractor import extractTextFromJpg, replace_backslashes
import json

app = FastAPI()

img_folder = "./images/"

# Request inicial
@app.get("/")
def hello_world_root():
    return {"Hello": "World"}

# Retorna o documento das imagens
@app.get("/images/{document_name}")
async def get_images_path(document_name: str):
    folder_path = "images/" + document_name
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(f"http://127.0.0.1:8000/{root}/{file}")
    
    return replace_backslashes(file_paths)

# Retorna as imagens
@app.get("/images/{document_name}/{image_name}")
async def get_image(document_name: str, image_name: str):
    image_path = "./images/" + document_name + "/" + image_name

    if not os.path.isfile(image_path):
        { "error": "Image not found" }

    return FileResponse(image_path)

# Retorna os indicares gerados pela IA
@app.get("/indicators/{document_name}")
async def get_indicators(document_name: str):
    print(document_name)
    print(img_folder)
    print(img_folder + document_name)
    files = extractTextFromJpg(img_folder + document_name)
    # return files

    full_text = ""
    for file in files:
        full_text += file
    print(full_text)
    return full_text

    response = ask_to_ai(full_text)
    json_object = json.loads(response.strip())

    return json_object

@app.get("/apresentacao/desafio/{dificuldade}")
async def get_desafio(dificuldade: str):
    recortes_path = "./recortes/" + dificuldade

    file_url = "apresentacao/desafio/" + dificuldade

    file_paths = []
    for root, dirs, files in os.walk(recortes_path):
        for file in files:
            file_paths.append(f"http://127.0.0.1:8000/{file_url}/{file}")
    
    files = extractTextFromJpg(recortes_path)
    
    file_paths = replace_backslashes(file_paths)
    # full_text = ""
    json_object = {}
    i = 0
    for file in files:
        json_object[file_paths[i]] = file
        i = i + 1

    return json_object
    
    # return file_paths

@app.get("/apresentacao/desafio/{dificuldade}/{recorte}")
async def get_recorte_desafio(dificuldade: str, recorte: str):
    image_path = "./recortes/" + dificuldade + "/" + recorte

    # if not os.path.isfile(image_path):
    #     { "error": "Image not found" }

    return FileResponse(image_path)
