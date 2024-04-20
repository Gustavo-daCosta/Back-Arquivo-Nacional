import cv2
import pytesseract
import os

# pytesseract config
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def enumerate_lines(text):
    lines = text.splitlines()
    if not lines:
        return text
    
    # Remove todas as linhas vazias
    strip_lines = [line for line in text.splitlines() if line.strip()]
    
    numbered_lines = [f"{i + 1} - {line}" for i, line in enumerate(strip_lines)]
    numbered_text = '\n'.join(numbered_lines)
    return numbered_text

def add_line_numbers(match):
    return f"{match.start() // len(match.group()) + 1} - {match.group()}"

# Função para a lógica de extração do texto
def extractTextFromJpg(path):
    # se o caminho for de uma pasta, significa que o texto está contido
    # em mais de uma página, logo, é necessário que função seja chamada
    # uma vez para cada página
    if os.path.isdir(path):
        files_path = get_files(path)
        texts = []
        i = 0
        for file in files_path:
            i = i + 1
            text = extractText(file)
            texts.append(text)
            if i == 5: break
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


# FÁCIL: historia-aikewara-indigena-sororo
# MÉDIO: autuacao
# DIFÍCIL: servico-censura-diversoes-publicas

# files = extractTextFromJpg()

# full_text = ""
# for file in files:
#     full_text += file

# enumerated_text = enumerate_lines(full_text)
# print(enumerated_text)
