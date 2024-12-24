from flask import Flask, render_template, request
import webbrowser
import logging
import os


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', status='Active')


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    try:
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            webbrowser.open("http://localhost:5000")    
        app.run()
    except Exception as e:
        logging.error("ERROR: ", exc_info=True)