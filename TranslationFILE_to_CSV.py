
import pandas as pd
import json
import PySimpleGUI as sg
from unidecode import unidecode as uni

# Read the JSON file
# with open('Spanish_New.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

def main():
    sg.theme('PythonPlus')

    layout = [[sg.T("")],
                [sg.Text("Upload the Translation JSON file: "), sg.Input(key="file_path"), sg.FileBrowse(key="file_path_browse")],
                [sg.T("")],
                [sg.Button("Submit", bind_return_key=True), sg.Button('Cancel')]]

    window = sg.Window('Main Menu', layout, size=(800, 180))

    while True:
        event, values = window.Read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Submit':
            json_file = values['file_path']
            window.close()


    data = json.load(open(json_file, encoding="utf8"))


    # Transform the data
    transformed_data = []
    for key, value in data['full'].items():
        transformed_data.append({
            'English': key,
            'Spanish': uni(value)  # Replace Unicode with accented letters
        })
        transformed_data.append({})

    # Create a DataFrame
    df = pd.DataFrame(transformed_data)

    # Save the DataFrame to a CSV file
    df.to_csv('Full_ES_Translation.csv', index=False, encoding='utf-8-sig')


if __name__=='__main__':
    main()



