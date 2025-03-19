# Audio Denoising Autoencoder

A Flask-based web application that uses deep learning autoencoders to remove noise from audio files. The application supports multiple types of noise (Gaussian, White, and Background) and provides an intuitive web interface for audio processing.

## 📁 Repository Structure

```
.
├── denoising_encoder_flask/     # Main Application Directory
│   ├── app.py                  # Flask application
│   ├── Dockerfile              # Docker configuration
│   ├── requirements.txt        # Python dependencies
│   ├── models/                 # Trained ML models
│   │   ├── denoising_autoencoder.h5
│   │   └── best_autoencoder_model.h5
│   ├── assets/                 # Asset files
│   │   └── background_noise.m4a
│   ├── templates/              # HTML templates
│   │   ├── index.html
│   │   └── result.html
│   ├── uploads/               # Temporary upload directory
│   ├── original_audio/        # Original audio storage
│   ├── noisy_audio/          # Noisy audio storage
│   └── denoised_audio/       # Processed audio storage
```

## 🚀 Setup and Installation

### Prerequisites

- Docker
- Git

### Application Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd denoising_encoder_flask
```

2. Build the Docker image:
```bash
docker build -t denoising-encoder .
```

3. Run the application:
```bash
docker run -p 6767:6767 \
    -v $(pwd)/uploads:/app/uploads \
    -v $(pwd)/original_audio:/app/original_audio \
    -v $(pwd)/noisy_audio:/app/noisy_audio \
    -v $(pwd)/denoised_audio:/app/denoised_audio \
    denoising-encoder
```

The web interface will be available at `http://localhost:6767`

## 🖥️ Using the Application

The web interface allows you to:
- Upload audio files (WAV format)
- Select noise type (Gaussian, White, or Background)
- Choose between basic and advanced denoising models
- Listen to original, noisy, and denoised audio
- Download processed audio files

### Supported Features

1. **Multiple Noise Types**
   - Gaussian Noise
   - White Noise
   - Background Noise

2. **Two Denoising Models**
   - Basic Autoencoder
   - Advanced Autoencoder

3. **Audio Processing**
   - Real-time audio playback
   - Download options for all audio versions
   - Automatic audio length adjustment

## 📊 Input Format

The application accepts:
- Audio files in WAV format
- Recommended duration: 2-10 seconds
- Any sample rate (automatically resampled)

## 🔍 Troubleshooting

Common issues and solutions:

1. **Docker container fails to start**
   - Check if port 6767 is available
   - Ensure model files are in the correct location
   - Verify Docker is running

2. **Audio processing errors**
   - Verify input file format is WAV
   - Check if file is corrupted
   - Ensure sufficient disk space for processing

## 📜 Application Flow


```mermaid
graph TD
    %% Main components
    User([User])
    Browser[Web Browser]
    Flask[Flask Web Server]
    
    %% Processing components
    AudioProcessor[Audio Processing Engine]
    NoiseGenerator[Noise Generator]
    
    %% Models
    subgraph ModelsModule
        BasicModel[Basic Autoencoder Model]
        AdvancedModel[Advanced Autoencoder Model]
    end
    
    %% Storage components
    subgraph StorageModule
        UploadsDir[Uploads Directory]
        OriginalDir[Original Audio Directory]
        NoisyDir[Noisy Audio Directory]
        DenoisedDir[Denoised Audio Directory]
    end
    
    %% External assets
    BackgroundNoise[Background Noise File]
    
    %% Routes/Endpoints
    subgraph RoutesModule
        IndexRoute["/Route"]
        DenoiseRoute["/denoise Route"]
        DownloadRoute["/download Route"]
    end
    
    %% User Flow
    User -->|Interacts with| Browser
    Browser -->|Sends requests to| Flask
    
    %% Main application flow
    Flask -->|Serves| IndexRoute
    IndexRoute -->|Renders| Browser
    
    Browser -->|Uploads audio file| DenoiseRoute
    DenoiseRoute -->|Saves file to| UploadsDir
    DenoiseRoute -->|Processes audio| AudioProcessor
    
    %% Audio processing flow
    AudioProcessor -->|Applies noise| NoiseGenerator
    NoiseGenerator -->|Uses| BackgroundNoise
    
    AudioProcessor -->|Saves original| OriginalDir
    AudioProcessor -->|Saves noisy| NoisyDir
    
    %% Model selection and processing
    AudioProcessor -->|Selects model| ModelsModule
    BasicModel -->|Processes noisy audio| DenoisedDir
    AdvancedModel -->|Processes noisy audio| DenoisedDir
    
    %% Results flow
    DenoisedDir -->|Provides results| DenoiseRoute
    DenoiseRoute -->|Renders results| Browser
    
    %% Download flow
    Browser -->|Requests file| DownloadRoute
    DownloadRoute -->|Retrieves from| StorageModule
    DownloadRoute -->|Sends file to| Browser
    Browser -->|Presents to| User
    
    %% Styling
    classDef main fill:#f7fafc,stroke:#4299e1,color:#4a5568
    classDef process fill:#4a5568,stroke:#4a5568,color:white
    classDef model fill:#c3cfe2,stroke:#4299e1,color:black
    classDef storage fill:#e2e8f0,stroke:#4299e1,color:#4a5568
    classDef route fill:#f7fafc,stroke:#4299e1,color:#4a5568

    class User,Browser,Flask main
    class AudioProcessor,NoiseGenerator process
    class BasicModel,AdvancedModel model
    class UploadsDir,OriginalDir,NoisyDir,DenoisedDir,BackgroundNoise storage
    class IndexRoute,DenoiseRoute,DownloadRoute route

    %% Subgraph styling
    classDef subgraphStyle fill:#f7fafc,stroke:#4299e1,color:#4a5568
    class ModelsModule,StorageModule,RoutesModule subgraphStyle

```
```mermaid
graph TD
    A[Web Browser] -->|Upload Audio| B[Flask Interface]
    B -->|Process| C[Audio Processing]

    subgraph ProcessingPipeline["Processing Pipeline"]
        C -->|Add Noise| D[Noise Generation]
        D -->|Denoise| E[Autoencoder Model]
        E -->|Save| F[File Management]
    end

    F -->|Response| B
    B -->|Display Results| A

    subgraph StorageModule["Storage"]
        G[Original Audio] -.->|Save| F
        H[Noisy Audio] -.->|Save| F
        I[Denoised Audio] -.->|Save| F
    end

    %% Apply classes
    class A,B interface
    class C,D,F process
    class E model
    class G,H,I storage

    %% Define class styles
    classDef interface fill:#f7fafc,stroke:#4299e1,color:#4a5568
    classDef process fill:#4a5568,stroke:#4a5568,color:white
    classDef storage fill:#e2e8f0,stroke:#4299e1,color:#4a5568
    classDef model fill:#c3cfe2,stroke:#4299e1,color:black


```
## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
