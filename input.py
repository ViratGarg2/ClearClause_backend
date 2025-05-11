from flask import request

def get_input():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return None, "No file selected"
        text = file.read().decode('utf-8')
    elif 'text' in request.form:
        text = request.form['text']
    else:
        return None, "No input provided"
    return text, None