from googletrans import Translator
from bs4 import BeautifulSoup
import os

def read_html_files(parent_dir):
    html_files = []
    for dirpath, dirnames, filenames in os.walk(parent_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                html_files.append(os.path.join(dirpath, filename))
    return html_files

def translate_html_file(filename, dest='hi'):
    # Load HTML file
    with open(filename, 'r') as file:
        html = file.read()

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Get all text from the HTML
    text_nodes = soup.findAll(text=True)

    # Translate text to Hindi using Google Translate
    translator = Translator()
    for text_node in text_nodes:
        # Ignore script and style tags
        if text_node.parent.name in ['script', 'style']:
            continue
        # Translate text and replace in the HTML
        translated_text = translator.translate(text_node.text, dest='hi').text
        # Replace original text with translated text
        text_node.replace_with(translated_text)

    # Write the translated HTML to a file
    with open(filename, 'w') as file:
        file.write(str(soup))

parent_dir = './trialtask'
html_files = read_html_files(parent_dir)
for html_file in html_files:
    print(html_file)
    translate_html_file(html_file)
