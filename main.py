import cv2
import pytesseract
import os
from pdf2image import convert_from_path
from dotenv import dotenv_values
from openai import OpenAI

# Carrega as variáveis de ambiente
enviroment = dotenv_values(".env")

# Converter pdf para imagens
# pdf2image / poppler config
poppler_path = "./Poppler/poppler-24.02.0/Library/bin"
images_path = "./assets/certidao-nascimento.pdf"

title = os.path.basename(images_path)
title = os.path.splitext(title)[0] # remove extension

assets_folder = "./assets/"
if (os.path.exists(assets_folder + title) == False):
    os.mkdir(assets_folder + title)

# até aqui funcionando

path = assets_folder + title + "/"
images = convert_from_path(images_path, poppler_path=poppler_path)

for i in range(len(images)):
    images[i].save(path + 'page' + str(i) + '.jpg', 'JPEG')
print("Concluído!")
print("Visite a pasta: " + path)










# pytesseract config
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Função para a lógica de extração do texto
def extractTextFromJpg(path):
    # se o caminho for de um arquivo, significa que todo o texto está contido
    # em somente uma página
    if os.path.isfile(path):
        text = extractText(path)
        return text
    
    # se o caminho for de uma pasta, significa que o texto está contido
    # em mais de uma página, logo, é necessário que função seja chamada
    # uma vez para cada página
    elif os.path.isdir(path):
        files_path = get_files(path)
        texts = []
        for file in files_path:
            text = extractText(file)
            texts.append(text)
        return texts

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


def ask_to_llm(prompt):
    client = OpenAI(
        api_key = enviroment["API_KEY"],
        base_url='https://api.together.xyz/v1',
    )

    chat = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": """Eu irei te dar um texto, preciso que você leia este texto e me retorne uma lista de indicadores sociais nos quais esse texto se encaixa.

            Definição dos possíveis marcadores: 

            1. Título
Tipo: Textual
Objetivo: Identificar nominalmente o documento.
Comentários: Registrar o título original. Caso isso não seja possível, atribuir um título elaborado
a partir de elementos de informação presentes na unidade que está sendo descrita, obedecidas
as convenções previamente estabelecidas.
Exemplo: Visita de Júlio Argentino Roca, ex-presidente da República Argentina, ao Museu
Nacional.

2. Data(s)
Tipo: Numérico
Objetivo: Informar a(s) data(s) da unidade de descrição.
Comentários: Fornecer a data a partir dos elementos de identificação cronológicos pelo qual
se indica a data em que o documento foi produzido ou dos elementos de identificação
cronológica do assunto de um documento. Informar o ano e, quando apropriado, dia e mês;
indicar, entre colchetes, as datas atribuídas. Em caso de dúvida, acrescente um ponto de
interrogação; use algarismos arábicos; Caso se disponha para a unidade de descrição apenas
de referência a século e/ou década, atribuir a data usando o(s) primeiro(s) algarismo(s)
correspondente(s) ao século e à década, completando com traço (–) os dados ignorados ou,
quando se puder identificar um período provável, atribuir datas-limite;
Exemplo: 1950-1975; 8/2/1890-18/4/1890; [1960?]-[1968?]; 01/01/2000;

3. Âmbito e conteúdo
Tipo: Texto
Objetivo: Fornecer aos usuários informações relevantes ou complementares ao Título o
documento.
Comentários: Informar o âmbito (contexto histórico e geográfico) e o conteúdo (tipologia
documental, assunto e estrutura da informação) da unidade de descrição. Eventos históricos e
naturais tais como guerras, revoluções, estações do ano e catástrofes podem ser utilizados
como marcos da contextualização histórica.
Exemplo: Planta cadastral, mostrando o núcleo urbano - sem nomear ruas - e os proprietários
da periferia, quando indica os seus nomes. Mostra, delimitando, os terrenos da colônia Argelina
(fundada na década de 1860 por franceses de origem argelina), Colônia Abranches (fundada em
novembro de 1873 por poloneses e islandeses) e parte da Colônia Dantas (fundada por

MANUAL HackathAN

5
italianos); trecho longo do rio Barigui; marcos, edificações, igrejas, estação ferroviária, chácara
do Barão de Capanema, parte da fazenda Beiro Alto.

4. Pontos de acesso e indexação de assuntos
Tipo: Lista
Objetivo: Registrar os procedimentos para recuperação do conteúdo de determinados
elementos de descrição, por meio da geração e elaboração de índices baseados em entradas
autorizadas e no controle do vocabulário adotado.
Comentários: Identificar os pontos de acesso que exigirão maior atenção na geração de índices
e realizar a indexação de assuntos de maneira controlada sobre elementos de descrição
estratégicos para a pesquisa. A indexação dos assuntos deve contemplar nomes de entidades
(Pessoas, entidades coletivas e famílias), eventos, áreas geográficas, períodos e assuntos
tópicos (geográficos).
Um arquivo de vocabulário controlado está sendo disponibilizado, no qual o campo(ponto de
acesso e indexação de assuntos) deve ser utilizado na função autocompletar. Caso o termo não
seja encontrado, ele deverá ser adicionado à base de dados para uso futuro.
Exemplos: Segunda Guerra Mundial, 1939-1945;
A Notícia (Jornal);
Cachambi (Rio de Janeiro, RJ)
Aragão, Antônio Renato, 1935-
Ministério da Fazenda (Brasil), 1808-2019

MARCADORES SOCIAIS

Tipo: Texto
Objetivo: Informar marcadores sociais com ênfase em gênero, raça e regionalidade
Comentários: Fornecer, a partir do conteúdo informacional do documento, marcadores sociais
com ênfase em gênero, raça e regionalidade. Entrada de marcadores de forma livre, a partir da
perspectiva da folksonomia. Folksonomia é o resultado da classificação, a partir do linguajar
natural da comunidade que a utiliza, por meio de tagueamento de um documento, visando à
sua recuperação. Restringir linguagem imprópria.
Marcadores: Homossexual; Homossexualidade; Homofobia; LGBTfobia; Feminismo, Mulheres,
Movimento Negro, Solano Trindade, Negro.
            
            
            Me retorne neste formato:

            [
                "indicador social 1"
                "indicador social 2"
                "indicador social 3"
            ]
            """,
        },
        {
            "role": "user",
            "content": prompt,
        }
        ],
        model="mistralai/Mixtral-8x7B-Instruct-v0.1"
    )

    return chat.choices[0].message.content


# path = "./contracts/contract-completo"

files = extractTextFromJpg(path)

full_text = ""

if (os.path.isfile(path)):
    full_text = files
elif (os.path.isdir(path)):
    for file in files:
        full_text += file



# print(full_text)
enumerated_text = enumerate_lines(full_text)
# print(enumerated_text)

response = ask_to_llm(prompt=full_text)
print(response)
