import cv2
import pytesseract
from dotenv import dotenv_values
import os


# Carrega as variáveis de ambiente
enviroment = dotenv_values(".env")
# pytesseract config
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Função para a lógica de extração do texto
def extractTextFromJpg(path):
    # se o caminho for de uma pasta, significa que o texto está contido
    # em mais de uma página, logo, é necessário que função seja chamada
    # uma vez para cada página
    if os.path.isdir(path):
        files_path = get_files(path)
        texts = []
        for file in files_path:
            text = extractText(file)
            texts.append(text)
        return texts
    # se o caminho for de um arquivo, significa que todo o texto está contido
    # em somente uma página
    elif os.path.isfile(path):
        text = extractText(path)
        return text

# Função que efetivamente extrai o texto (sim eu sei que os nomes estão confusos)
def extractText(path):
    image = cv2.imread(path)
    # Transforma todas as cores da imagem em cinza para evitar problemas de reconhecimento relacionados a cor ou iluminação
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(threshold_image)
    return text


# Função para pegar o path de todos os arquivos que estão dentro de uma pasta
def get_files(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    
    return replace_backslashes(file_paths)

# Quando pegamos o path dos arquivos, a divisão vem com "\\",
# essa regex troca todas as ocorrências de "\\" para "/"
# e faz isso para cada arquivo na lista de paths
# OBS: Função utilizada unicamente quando o path é uma pasta
def replace_backslashes(folder_path):
    file_paths = []
    for file in folder_path:
        file_paths.append(file.replace("\\", "/"))
        
    return file_paths


path = "./assets/certidao-nascimento"
full_text = ""
files = extractTextFromJpg(path)

if (os.path.isfile(path)):
    full_text = files
elif (os.path.isdir(path)):
    for file in files:
        print("VAI SE FUDER SUPER AUTISMO")
        print(file)
        full_text += file



# print(full_text)
