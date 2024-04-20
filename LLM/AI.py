from openai import OpenAI
from dotenv import dotenv_values

# Carrega as variáveis de ambiente
enviroment = dotenv_values(".env")

def ask_to_ai(prompt):
    client = OpenAI(
        api_key = enviroment["API_KEY"],
        base_url='https://api.together.xyz/v1',
    )

    chat = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": """Eu irei te dar um texto, preciso que você leia este texto e me retorne uma lista de indicadores sociais nos quais esse texto se encaixa.
            ATENÇÃO: POR FAVOR ME RESPONDA EM PORTUGUÊS BRASILEIRO

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
novembro de 1873 por poloneses e islandeses) e parte da Colônia Dantas (fundada por italianos); trecho longo do rio Barigui; marcos, edificações, igrejas, estação ferroviária, chácara
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
            
            
            RETORNE O RESULTADO NESTE FORMATO, DE JSON:
            {
                "indicador social 1": "trecho do texto de onde o indicador foi retirado"
                "indicador social 2": "trecho do texto de onde o indicador foi retirado"
                "indicador social 3": "trecho do texto de onde o indicador foi retirado"
            }

            Gostaria também que, para cada indicador, você me retornasse o trecho do texto que faz referência a esse indicador

            ATENÇÃO: RETORNE EXCLUSIVAMENTE O JSON E MAIS NADA, APENAS O JSON
            """,
        },
        {
            "role": "user",
            "content": prompt,
            "max_new_tokens": 8000
        }
        ],
        model="MISTRALAI/MIXTRAL-8X7B-INSTRUCT-V0.1",
    )

    return chat.choices[0].message.content
