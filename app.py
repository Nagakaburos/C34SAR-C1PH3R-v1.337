from flask import Flask, render_template, request, session, redirect, url_for
import os
import unicodedata

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'uma_chave_secreta_muito_segura')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def remove_accents(text):
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if not unicodedata.combining(c)).lower()

def caesar(original_text, shift_amount, operation):
    processed_text = remove_accents(original_text)
    result = []
    
    shift = shift_amount if operation == 'encrypt' else -shift_amount
    shift %= 26
    
    for char in processed_text:
        if char not in alphabet:
            result.append(char)
            continue
            
        original_index = alphabet.index(char)
        new_index = (original_index + shift) % 26
        result.append(alphabet[new_index])
    
    return ''.join(result)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        shift = int(request.form['shift'])
        action = request.form['action']
        
        result = caesar(text, shift, action)
        session['result'] = result
        return redirect(url_for('index'))
    
    result = session.pop('result', None)
    return render_template('index.html', result=result)

@app.route('/clear', methods=['POST'])
def clear():
    session.pop('result', None)
    return '', 204

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True)