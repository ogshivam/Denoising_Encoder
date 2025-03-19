from flask import Flask, request, send_file, render_template, url_for
import os
import numpy as np
import librosa
import tensorflow as tf
import soundfile as sf
from werkzeug.utils import secure_filename
import warnings
warnings.filterwarnings('ignore')

# At the top of your app.py, after the imports
# Update this line
app = Flask(__name__)  # Remove the template_folder parameter

# Update configuration with new directories
app.config['UPLOAD_FOLDER'] = '/Users/shivampratapwar/Downloads/Encoders/denoising_encoder_flask/uploads'
app.config['ORIGINAL_FOLDER'] = '/Users/shivampratapwar/Downloads/Encoders/denoising_encoder_flask/original_audio'
app.config['NOISY_FOLDER'] = '/Users/shivampratapwar/Downloads/Encoders/denoising_encoder_flask/noisy_audio'
app.config['DENOISED_FOLDER'] = '/Users/shivampratapwar/Downloads/Encoders/denoising_encoder_flask/denoised_audio'

# Create all required directories
for folder in [app.config['UPLOAD_FOLDER'], 
              app.config['ORIGINAL_FOLDER'],
              app.config['NOISY_FOLDER'],
              app.config['DENOISED_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

NOISE_FILE = 'assets/background_noise.m4a'
ALLOWED_EXTENSIONS = {'wav', 'm4a'}
SAMPLING_RATE = 44100
DURATION = 2
EXPECTED_SHAPE = SAMPLING_RATE * DURATION


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_gaussian_noise(audio, noise_factor=0.02):
    noise = np.random.normal(0, noise_factor, audio.shape)
    return np.clip(audio + noise, -1.0, 1.0)

def add_white_noise(audio, noise_factor=0.05):
    noise = np.random.uniform(-noise_factor, noise_factor, audio.shape)
    return np.clip(audio + noise, -1.0, 1.0)

def add_background_noise(audio, noise_audio):
    noise_audio = noise_audio[:len(audio)]
    noise_audio = noise_audio * 0.3  # Adjust noise intensity
    return np.clip(audio + noise_audio, -1.0, 1.0)

def process_audio(file_path, noise_type):
    try:
        audio, _ = librosa.load(file_path, sr=SAMPLING_RATE, res_type='kaiser_best')
        
        # Ensure 2-second duration
        if len(audio) < EXPECTED_SHAPE:
            audio = np.pad(audio, (0, EXPECTED_SHAPE - len(audio)))
        elif len(audio) > EXPECTED_SHAPE:
            audio = audio[:EXPECTED_SHAPE]
        
        # Normalize
        audio = audio / np.max(np.abs(audio))
        
        # Load background noise if needed
        if noise_type == 'background':
            background_noise, _ = librosa.load(NOISE_FILE, sr=SAMPLING_RATE)
            noisy_audio = add_background_noise(audio, background_noise)
        elif noise_type == 'gaussian':
            noisy_audio = add_gaussian_noise(audio)
        elif noise_type == 'white':
            noisy_audio = add_white_noise(audio)
        else:
            noisy_audio = audio  # No noise added
        
        return noisy_audio
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/denoise', methods=['POST'])
def denoise():
    try:
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        model_choice = request.form.get('model', 'basic')
        noise_type = request.form.get('noise', 'white')
        
        if file.filename == '' or not allowed_file(file.filename):
            return 'Invalid file', 400
        
        # Save and process original audio
        filename = secure_filename(file.filename)
        base_filename = os.path.splitext(filename)[0]
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Process original audio
        original_filename = f'original_{base_filename}.wav'
        original_path = os.path.join(app.config['ORIGINAL_FOLDER'], original_filename)
        original_audio = process_audio(upload_path, 'none')
        sf.write(original_path, original_audio, SAMPLING_RATE, format='WAV')
        
        # Process noisy audio
        noisy_audio = process_audio(upload_path, noise_type)
        noisy_filename = f'noisy_{base_filename}.wav'
        noisy_path = os.path.join(app.config['NOISY_FOLDER'], noisy_filename)
        sf.write(noisy_path, noisy_audio, SAMPLING_RATE, format='WAV')
        
        # Process denoised audio
        noisy_input = noisy_audio.reshape(1, -1)
        model = advanced_model if model_choice == 'advanced' else basic_model
        denoised_audio = model.predict(noisy_input, verbose=0).reshape(-1)
        denoised_filename = f'denoised_{base_filename}.wav'
        denoised_path = os.path.join(app.config['DENOISED_FOLDER'], denoised_filename)
        sf.write(denoised_path, denoised_audio, SAMPLING_RATE, format='WAV')
        
        return render_template('result.html',
                             original=original_filename,
                             noisy=noisy_filename,
                             denoised=denoised_filename)

    except Exception as e:
        return f'Error processing audio: {str(e)}', 500

@app.route('/download/<filename>')
def download_file(filename):
    # Determine which folder to use based on filename prefix
    if filename.startswith('original_'):
        folder = app.config['ORIGINAL_FOLDER']
    elif filename.startswith('noisy_'):
        folder = app.config['NOISY_FOLDER']
    elif filename.startswith('denoised_'):
        folder = app.config['DENOISED_FOLDER']
    else:
        return 'Invalid file', 400
        
    return send_file(os.path.join(folder, filename), as_attachment=True)

if __name__ == '__main__':
    # Load models
    try:
        basic_model = tf.keras.models.load_model('models/denoising_autoencoder.h5', compile=False)
        basic_model.compile(optimizer='adam', loss='mse')
        advanced_model = tf.keras.models.load_model('models/best_autoencoder_model.h5', compile=False)
        advanced_model.compile(optimizer='adam', loss='mse')
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        raise
    
    app.run(host='0.0.0.0', port=6767, debug=True)
