from googletrans import Translator
from bs4 import BeautifulSoup
import os
import time

stored = {}

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
    # text_nodes = soup.findAll(text=True)
    text_nodes = soup.findAll(string=True)

    # Translate text to Hindi using Google Translate
    translator = Translator()
    for text_node in text_nodes:
        # Ignore script and style tags
        # print('text_node.text', f"aaa{text_node.text}aaa", not text_node.text, text_node.text == '\n')
        if text_node.parent.name in ['script', 'style'] or not text_node.text or text_node.text == '\n':
            continue
        # print(text_node)
        # Translate text and replace in the HTML
        if not stored.get(text_node.text):
            while True:
                try:
                    translated_text = translator.translate(text_node.text, dest='hi').text
                    break
                except Exception as e:
                    print(e) 
                    time.sleep(60)
                # Replace original text with translated text
            stored[text_node.text] = translated_text
            time.sleep(1)
        else:
            translated_text = stored[text_node.text]
        text_node.replace_with(translated_text)
        # print(translated_text)

    # Write the translated HTML to a file
    with open(filename, 'w') as file:
        file.write(str(soup))


if __name__ == "__main__":
    parent_dir = './classcentral'
    html_files = read_html_files(parent_dir)
    n = len(html_files)
    for i, html_file in enumerate(html_files):
        print(f"{i}/{n} {html_file}")
        translate_html_file(html_file)

