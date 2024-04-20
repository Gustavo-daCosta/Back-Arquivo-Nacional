import os
from pdf2image import convert_from_path

# pdf2image / poppler config
poppler_path = "./Poppler/poppler-24.02.0/Library/bin"
path = "../documents/"

files_names = os.listdir(path)

title_extension = ""
title = ""
index = ""

def select_file():
    path = "../documents/"
    while True:
        # try:
        print("SELECIONE UM ARQUIVO:")
        i = 0
        for file in files_names:
            i = i + 1
            title_extension = os.path.basename(file)
            title = os.path.splitext(title_extension)[0] # remove extension
            print(f" {i}  - {title}")

        print("\nDigite o número corresponde ao arquivo.")
        index = int(input("Número: "))
        title_extension = os.path.basename(files_names[index - 1])
        title = os.path.splitext(title_extension)[0]
        path = path + title_extension
        break
        # except:
        #     print("ERRO! Digite um número válido.")
        #     input("Aperte ENTER para continuar...")
        #     os.system('cls')


    images_folder = "../images/"
    folder_path = images_folder + title + "/"

    if (not os.path.exists(folder_path)):
        os.mkdir(folder_path)
        print("\n * Convertendo pdf para imagens... *")
        images = convert_from_path(path, poppler_path=poppler_path)

        for i in range(len(images)):
            file_name = folder_path + title + '-pg' + str(i + 1) + '.jpg'
            images[i].save(file_name, 'JPEG')
        print("Concluído!")
        print("Visite a pasta: " + folder_path)

    print(folder_path)


select_file()

# images = convert_from_path(path, poppler_path=poppler_path)

# for i in range(len(images)):
#     file_name = "../images" + title + '-pg' + str(i + 1) + '.jpg'
#     images[i].save(file_name, 'JPEG')