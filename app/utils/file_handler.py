import PyPDF2
import markdown

def extract_text(filepath):
    if filepath.endswith('.pdf'):
        return _extract_pdf_text(filepath)
    elif filepath.endswith('.md'):
        return _extract_markdown_text(filepath)
    elif filepath.endswith('.txt'):
        return _extract_text_file(filepath)
    else:
        return None

import PyPDF2

def _extract_pdf_text(filepath):
    text = []
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text.append(page.extract_text())
    
    # # Print the extracted text
    # print("Extracted Text:", text)
    
    return text


def _extract_markdown_text(filepath):
    with open(filepath, 'r') as file:
        html = markdown.markdown(file.read())
    return [html]

def _extract_text_file(filepath):
    with open(filepath, 'r') as file:
        return file.readlines()
