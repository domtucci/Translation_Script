
import pandas as pd
import json
import PySimpleGUI as sg
from unidecode import unidecode as uni
import argparse
from pathlib import Path

# Read the JSON file
# with open('Spanish_New.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Choose between GUI and command line")
    parser.add_argument("-v", "--pysimple", action="store_true", help="Use the GUI if you have PySimpleGUI")
    #parser.add_argument("-c", "--command", type=str, help="Specify the JSON file path for command line mode")

    # File input
    parser.add_argument("-f", "--file", type=str, help="Path to the JSON config file")


    args = parser.parse_args()

    # Read file path

    if args.pysimple:
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

    elif args.file:           
        json_file = Path(args.file)



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



