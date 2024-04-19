#can you create a python script that replaces the spanish unicodes in a JSON file
#this will correctly make the accent marked letters 

import PySimpleGUI as sg

# Read the JSON file
# with open('Spanish_New.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

def main():
    sg.theme('PythonPlus')

    layout = [[sg.T("")],
              [sg.Text("Upload the Translation TEXT file: "), sg.Input(key="file_path"), sg.FileBrowse(key="file_path_browse")],
              [sg.T("")],
              [sg.Button("Submit", bind_return_key=True), sg.Button('Cancel')]]

    window = sg.Window('Main Menu', layout, size=(800, 180))

    while True:
        event, values = window.Read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Submit':
            text_file = values['file_path']
            window.close()
            process_text_file(text_file)


def replace_unicode(text):
    replacements = {
        r'\u00a1': '¡',
        r'\u00bf': '¿',
        r'\u00e1': 'á',
        r'\u00c1': 'Á',
        r'\u00e4': 'ä',
        r'\u00c4': 'Ä',
        r'\u00e9': 'é',
        r'\u00c9': 'É',
        r'\u00eb': 'ë',
        r'\u00cb': 'Ë',
        r'\u00ed': 'í',
        r'\u00cd': 'Í',
        r'\u00ef': 'ï',
        r'\u00cf': 'Ï',
        r'\u00f3': 'ó',
        r'\u00d3': 'Ó',
        r'\u00f6': 'ö',
        r'\u00d6': 'Ö',
        r'\u00fa': 'ú',
        r'\u00da': 'Ú',
        r'\u00dc': 'Ü',
        r'\u00fc': 'ü',
        r'\u00f1': 'ñ',
        r'\u00d1': 'Ñ',
        r'\u200b': '',
        r'\u0027': "'",
        r'\u2026': "..."
        # Add more Unicode replacements here
    }
    
    for unicode_str, char in replacements.items():
        text = text.replace(unicode_str, char)
    
    return text

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    replaced_text = replace_unicode(text)
    
    output_file_path = "replaced_text.txt"  # Change the output file path as needed
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(replaced_text)



if __name__ == '__main__':
    main()
