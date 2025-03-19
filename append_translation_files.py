import pandas as pd
import json
import PySimpleGUI as sg
from googletrans import Translator, constants
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Choose between GUI and command line")
    parser.add_argument("-v", "--pysimple", action="store_true", help="Use the GUI if you have PySimpleGUI")
    #parser.add_argument("-c", "--command", type=str, help="Specify the JSON file path for command line mode")

    # File input
    parser.add_argument("-n", "--file", type=str, help="Path to the navigation JSON file")
    parser.add_argument("-t", "--tran", type=str, help="Path to the translation JSON file")

    # Selection of language
    parser.add_argument("-l", "--language", type=str, choices=['Spanish', 'Creole'],
                        help="Specify the language: 'Spanish', or 'Creole'")

    args = parser.parse_args()

    # Read file path

    if args.pysimple:
        sg.theme('DarkTeal2')

        layout = [[sg.T("")],
                    [sg.Text("Upload the JSON version of the Navigation File: "), sg.Input(key="file_path"), sg.FileBrowse(key="file_path_browse_nav")],
                    [sg.Text('Upload the JSON version of the Translation File: '), sg.Input(key='translation_file'), sg.FileBrowse(key="file_path_browse_translator")],
                    [sg.Text('Please select your target language: '), sg.Listbox(values=['Spanish', 'Creole'], size=(12,1), key='target_language')],
                    [sg.T("")],
                    [sg.Button("Submit", bind_return_key=True), sg.Button('Cancel')]]

        window = sg.Window('Main Menu', layout, size=(800, 250))

        while True:
            event, values = window.Read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Submit':
                nav_file = values['file_path']
                translation_file = values['translation_file']
                target_language = values['target_language'][0]
                window.close()

    elif args.file:           
        nav_file = Path(args.file)           
        translation_file = Path(args.tran)
        target_language = args.language


    nav_data = json.load(open(nav_file))
    og_translation = json.load(open(translation_file, encoding='UTF-8'))
    new_translation = update_translation_file(nav_data, og_translation, target_language)
    og_translation['full'] = new_translation
    new_translation_json = json.dumps(og_translation)

    new_file_name = target_language+'_New.json'
    with open(new_file_name, 'w') as f:
        f.write(new_translation_json)


def update_translation_file(nav, original_translation, language):
    choices = []
    missing_phrases = []
    translated_phrases = []

    nav_df = pd.DataFrame(nav['questions'])
    text_list = list(nav_df.loc['text'])
    sources_list = list(nav_df.loc['source'])

    for i in range(0, len(sources_list)):
        if type(sources_list[i]) != dict:
            continue
        else:
            if 'list' not in sources_list[i].keys():
                continue
            else:
                choices.append(sources_list[i]['list'])

    translations = original_translation['full']
    english_phrases = list(translations.keys())

    for phrase in text_list:
        if phrase not in english_phrases:
            missing_phrases.append(phrase)
        else:
            continue
    for choice_list in choices:
        for choice in choice_list:
            if choice not in english_phrases:
                missing_phrases.append(choice)
            else:
                continue

    translator = Translator()

    if language == 'Spanish':
        for phrase in missing_phrases:
            translated_phrase = translator.translate(phrase, dest='es')
            translated_phrases.append(translated_phrase.text)
    elif language == 'Creole':
        for phrase in missing_phrases:
            translated_phrase = translator.translate(phrase, dest='ht')
            translated_phrases.append(translated_phrase.text)

    translated_dict = {missing_phrases[i]: translated_phrases[i] for i in range(len(missing_phrases))}
    translations.update(translated_dict)
    
    return translations

if __name__=='__main__':
    main()