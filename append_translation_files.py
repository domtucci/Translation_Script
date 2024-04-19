import pandas as pd
import json
import PySimpleGUI as sg
from deep_translator import GoogleTranslator
import time


def main():
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

    nav_data = json.load(open(nav_file))
    og_translation = json.load(open(translation_file, encoding='UTF-8'))
    new_translation = update_translation_file(nav_data, og_translation, target_language)
    og_translation['full'] = new_translation
    new_translation_json = json.dumps(og_translation)

    new_file_name = target_language+'_New_1.json'
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
        # create another if statement that tells the code 'if a digit exists skip it' therefore not translating. Reducing the amount of API calls.
        # we may be able to regex this
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

    if language == 'Spanish':
        for phrase in missing_phrases:
            translated_phrase = GoogleTranslator(source = 'auto', target = 'es').translate(text=phrase)
            translated_phrases.append(translated_phrase)
            time.sleep(1)
    elif language == 'Creole':
        for phrase in missing_phrases:
            translated_phrase = GoogleTranslator(source = 'auto', target = 'ht').translate(text=phrase)
            translated_phrases.append(translated_phrase)
            time.sleep(1)

    translated_dict = {missing_phrases[i]: translated_phrases[i] for i in range(len(missing_phrases))}
    translations.update(translated_dict)

    return translations

# def translate_with_retry(translator, phrase, dest, max_retries=3):
#     retries = 0
#     while retries < max_retries:
#         try:
#             translated = translator.translate(phrase, dest=dest)
#             return translated.text
#         except Exception as e:
#             print(f"Translation failed for '{phrase}'. Retrying...")
#             retries += 1
#     return None


if __name__=='__main__':
    main()

