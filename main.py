from googletrans import Translator
import PySimpleGUI as sg
from PIL import Image
import pytesseract, requests, languages

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tesseract_lang = languages.tesseract_lang
google_lang = languages.google_lang
sg.theme('LightPurple')

def window_exit_check(event):
	if event == sg.WINDOW_CLOSED:
		exit()

def error_window(e):
	error_layout = [
		[sg.Text(e)], 
		[sg.Button('Exit', size=(15,1))]
	]
	e_window = sg.Window('ERROR', error_layout, element_justification='center')
	e_window.read()
	exit()

def image_reader(value, choice, src_lang):
	text = ''
	if choice == 1:
		try:
			text = pytesseract.image_to_string(Image.open(requests.get(value, stream=True).raw), lang=src_lang)
		except Exception as e:
			error_window(e)
	else:
		text = pytesseract.image_to_string(Image.open(value), lang=src_lang)
 
	text2 = '\n'.join(line for line in iter(text.splitlines()) if not line.isspace() and not line=='')
	return text2

def translate_text(text, dest_lang):
	translator = Translator(service_urls = ['translate.googleapis.com'])
	lines = list(text.splitlines()) 

	results = translator.translate(lines, dest=dest_lang)
	s = ''
	for r in results:
		s += r.text
		s += '\n'
	return s

def main():
	
	original_text,translated_text = '', ''

	basic_layout = [
		[sg.Text('Select input choice', size=(30,1))],
		[sg.Button('URL', size=(15,1)), sg.Button('File', size=(15,1))]
	]

	src_language_layout = [
		[sg.Text('Choose source language (Language in image):'), sg.Combo(list(tesseract_lang.keys()), size=(20,1), key='-SRCLANGUAGE-')],
		[sg.Button('Next', size=(15,1))]
	]

	dest_language_layout = [
		[sg.Text('Choose destination language (Language to be translated into):'), sg.Combo(list(google_lang.keys()), size=(20,1), key='-DESTLANGUAGE-')],
		[sg.Button('Next', size=(15,1))]
	]

	url_layout = [
		[sg.Text('Enter Image URL')], 
		[sg.Input(key='-URL-')], 
		[sg.Button('Submit', size=(15,1))]
	]

	file_layout = [
		[sg.Text('Select File')],
		[sg.InputText(key='-FILENAME-'), sg.FileBrowse()],
		[sg.Button('Submit', size=(15,1))]
	]

	window = sg.Window('Image Translator', basic_layout, element_justification='c')

	event, values = window.read()
	window.close()
	window_exit_check(event)

	window = sg.Window('Language', src_language_layout, element_justification='c', resizable=True)

	e, values = window.read()
	window_exit_check(e)
	try:
		src_lang = tesseract_lang[values['-SRCLANGUAGE-']]
	except:
		error_window('Invalid language')
	window.close()

	window = sg.Window('Language', dest_language_layout, element_justification='c', resizable=True)

	e, values = window.read()
	window_exit_check(e)
	try:
		dest_lang = google_lang[values['-DESTLANGUAGE-']]
	except:
		error_window('Invalid language')
	window.close()
	
	if event == 'URL':
		window = sg.Window('Enter URL', url_layout, element_justification='c')
		event, values = window.read()
		window_exit_check(event)
		try:
			original_text = image_reader(values['-URL-'], 1, src_lang)
		except Exception as e:
			error_window(e)
		
	else:
		window = sg.Window('Select File', file_layout, element_justification='c')
		event, values = window.read()
		window_exit_check(event)
		try:
			original_text = image_reader(values['-FILENAME-'], 2, src_lang)
		except Exception as e:
			error_window(e)

	try:
		translated_text = translate_text(original_text, dest_lang)
	except Exception as e:
		sg.Window('ERROR', [[sg.Text(e)], [sg.Button('Exit')]]).read()
		exit()

	output_layout = [
		[sg.Text('Original Text:')],
		[sg.Text(original_text)],
		[sg.Text('Translated Text:')],
		[sg.Text(translated_text)],
		[sg.Button('OK', size=(15,1))]
	]

	window.close()
	window = sg.Window('Result', output_layout, element_justification='c')
	event, values = window.read()
	window.close()

if __name__ == '__main__':
	main()