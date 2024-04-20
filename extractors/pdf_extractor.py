from pdfquery import PDFQuery

def extract_text_from_pdf(pdf_path):
    pdf = PDFQuery(pdf_path)
    pdf.load()

    text = ""
    num_pages = len(list(pdf.tree.getroot().getiterator('LTPage')))
    for page_num in range(num_pages):
        pdf.tree.write('temp.xml', pretty_print=True)
        page_text = ""
        for element in pdf.tree.iter('LTTextLineHorizontal'):
            page_text += element.text.strip() + " "
            print("Quebra de linha")
        text += page_text + "\n"
    return text

# Example usage:
pdf_path = './assets/autuacao.pdf'
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)
