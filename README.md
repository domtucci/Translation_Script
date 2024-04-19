# Translation_Script

# append_translation_files
This python script is used to append translated text to the Spanish/Creole configuration files. The configuration file is used to translate our decision trees within the Rtasq database. It uses a Google Translate API call to translate the question text and any question choice from a list. Note: be sure your internet is running well or else the API calls will fail in the middle of running this program.

# TranslationFILE_to_CSV
A python scripted used for visual organization of config json spanish and creole files. All it does is put the English and Spanish text into separate columns of a csv file.

# Replacement_script
To finalize the translation config file this program will replace all unicodes with the proper characters. 
