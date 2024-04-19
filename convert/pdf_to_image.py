import os
from PIL import Image
from pdf2image import convert_from_path

# pdf2image / poppler config
poppler_path = "../Poppler/poppler-24.02.0/Library/bin"
title = "autuacao"

assets_folder = "../assets/"
if (os.path.exists(assets_folder + title) == False):
    os.mkdir(assets_folder + title)

# até aqui funcionando

images_path = "../assets/certidao-nascimento.pdf"
path = assets_folder + title + "/"
images = convert_from_path(images_path, poppler_path=poppler_path)

for i in range(len(images)):
    images[i].save(path + 'page' + str(i) + '.jpg', 'JPEG')
print("Concluído!")
print("Visite a pasta: " + path)
