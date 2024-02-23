from flask import Flask, flash, request, render_template, redirect, url_for, send_from_directory, session
import os
import logging
from werkzeug.utils import secure_filename
from model_training import train_linear_regression, visualize_training
import pickle
import datetime
import secrets

# initialize environment variables
from dotenv import load_dotenv

# Create a log file
now = datetime.datetime.now()
app_log = f'logs/app_{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'

# Configure logging
logging.basicConfig(filename=app_log, level=logging.INFO,
                    format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

load_dotenv()

# Initialize the Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['SECRET_KEY'] = secrets.token_hex(16)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.secret_key = app.config['SECRET_KEY']
#logging.info(f"Secret Key{app.config['SECRET_KEY']}")

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Ensure logs folder exists
os.makedirs('logs', exist_ok=True)

# Create a log file
now = datetime.datetime.now()
app_log = f'logs/app_{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'

# Configure logging
logging.basicConfig(filename=app_log, level=logging.INFO,
                    format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

ALLOWED_EXTENSTIONS = os.getenv('ALLOWED_FILE_TYPES')
logging.info(f"Allowed file extensions: {ALLOWED_EXTENSTIONS}")
logging.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")

def allowed_file(filename):
    logging.info(f"Checking if {filename} is allowed")
    logging.info(f"Allowed extensions: {ALLOWED_EXTENSTIONS}")
    logging.debug(f"File extension: {filename.rsplit('.', 1)[1].lower()}")
    logging.debug(f"types: filename {type(filename)} ALLOWED_EXTENSTIONS {type(ALLOWED_EXTENSTIONS)}")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSTIONS


@app.route('/')
def index():
    logging.info("Homepage accessed")
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        logging.info("File upload request received")
        file = request.files['file']
        if file and allowed_file(file.filename):
            logging.info(f"File {file.filename} is valid")
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File successfully uploaded')
            logging.info(f"File {file.filename} saved to {file_path}")
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Only CSV files are allowed.')
            logging.warning(f"Invalid file type. Only CSV files are allowed.")
    return render_template('upload.html')

@app.route('/linear-regression', methods=['GET', 'POST'])
def linear_regression():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            model_filename, mse, model, X, y = train_linear_regression(file_path, app.config['UPLOAD_FOLDER'])
            flash(f'Linear Regression Model trained. MSE: {mse}')
            logging.info(f"Linear Regression Model trained. MSE: {mse}")
            # Save the model
            #model_path = os.path.join(app.config['UPLOAD_FOLDER'], 'linear_regression_model.pkl')
            # visualize training
            #plot_filename = visualize_training(model, X, y, app.config['UPLOAD_FOLDER'])
            #plot_url = url_for('static', filename='uploads/' + plot_filename)
            #return render_template('training_sucess.html', mse = mse, model_filename = model_filename, plot_url = plot_url)
            return render_template('training_success.html', mse = mse, model_filename = model_filename)
    return render_template('linear_regression.html')

@app.route('/training-success')
def training_success():
    mse = session.get('mse', 'Unknown')
    model_filename = session.get('model_filename', 'Unknown')
    
    return render_template('training_success.html', mse = mse, model_filename = model_filename)


@app.route('/download/<filename>')
def download_model(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    
    logging.info(f"Starting the app on {host}:{port}\n"
                 f" with debug mode on"
                 f" and log file at {app_log}")
    print(f"Click to see: http://{host}:{port}\n") 
    
    app.run(host=host, port=port, debug=False)