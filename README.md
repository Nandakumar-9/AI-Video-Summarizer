# AI-Video-Summarizer

AI-Powered Multilingual Video Summarizer and Quiz Generator using Whisper, BART, FLAN-T5, and NLLB with Flask backend and React frontend.

---

# Project Structure

```text
AI-Video-Summarizer/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── outputs/
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── .gitignore
│
├── .gitignore
└── README.md
```

---

# Project Workflow

## Step 1 — Video Upload

User uploads a video from the React frontend.

---

## Step 2 — Audio Extraction

FFmpeg extracts audio from the uploaded video.

```text
Video → audio.wav
```

---

## Step 3 — Speech to Text

OpenAI Whisper converts audio into transcript text.

```text
audio.wav → transcript.txt
```

Model used:

```text
Whisper Small
```

---

## Step 4 — Summary Generation

BART generates a meaningful summary from transcript.

```text
transcript.txt → summary.txt
```

Model used:

```text
facebook/bart-large-cnn
```

---

## Step 5 — Quiz Generation

FLAN-T5 generates structured quiz questions from transcript.

```text
transcript.txt → quiz.txt
```

Model used:

```text
google/flan-t5-base
```

(Used for deployment stability on Hugging Face CPU)

---

## Step 6 — Translation

NLLB translates summary into selected target language.

Supported Languages:

* Telugu
* Hindi
* Tamil
* Kannada
* Malayalam
* English

Model used:

```text
facebook/nllb-200-distilled-600M
```

---

## Step 7 — Final Output

Frontend displays:

* Transcript Preview
* Summary Preview
* Quiz Questions
* Translated Summary

---

# Deployment Architecture

## Backend Deployment

Hosted on:

Hugging Face Spaces

Contains:

* Flask API
* Whisper
* BART
* FLAN-T5
* Translation Model
* FFmpeg
* `/upload` route

---

## Frontend Deployment

Hosted on:

Vercel

Contains:

* React UI
* Upload Button
* Language Selector
* Result Cards
* Loading UI

---

## Source Code

Hosted on:

GitHub

Repository includes:

* backend
* frontend
* README
* .gitignore

---

# Why This Deployment Path

## Correct Professional Structure

```text
Frontend → Vercel

Backend → Hugging Face Spaces

Code → GitHub
```

This is better than GitHub Pages because:

* backend needs Python + ML models
* GitHub Pages only supports static frontend hosting

---

# Getting Started with Create React App

This project frontend was bootstrapped with Create React App.

---

# Available Scripts

In the frontend project directory, you can run:

## npm start

Runs the app in development mode.

```text
http://localhost:3000
```

The page reloads automatically when changes are made.

You may also see lint errors in the console.

---

## npm test

Launches the test runner in the interactive watch mode.

Used for testing React components.

---

## npm run build

Builds the app for production to the `build` folder.

This correctly bundles React in production mode and optimizes the build for best performance.

The build is minified and filenames include hashes.

Used during Vercel deployment.

---

## npm run eject

This is a one-way operation.

Once you eject, you cannot go back.

It copies all internal React configuration files into your project.

Usually not required for this project.

---

# Future Improvements — Model Upgrades for Better Accuracy

For better accuracy and higher-quality results, the models can be upgraded or modified based on available hardware and deployment resources.

---

## 1. Speech-to-Text Improvement

### Current Model

```text
Whisper Small
```

### Upgrade Options

```text
Whisper Medium
Whisper Large
Whisper Large-v3
```

### Benefits

* better transcription accuracy
* improved speaker understanding
* better handling of accents
* improved punctuation
* stronger long-video performance

### Note

Larger Whisper models require more RAM and better hardware.

---

## 2. Summary Generation Improvement

### Current Model

```text
facebook/bart-large-cnn
```

### Upgrade Options

```text
google/pegasus-xsum
google/pegasus-cnn_dailymail
facebook/bart-large-cnn (fine-tuned)
```

### Benefits

* better summary quality
* more accurate key-point extraction
* reduced repetitive summarization
* improved contextual understanding

---

## 3. Quiz Generation Improvement

### Current Model

```text
google/flan-t5-base
```

### Upgrade Options

```text
google/flan-t5-large
google/flan-t5-xl
google/flan-t5-xxl
```

### Benefits

* better question framing
* more meaningful quiz generation
* less repetition
* stronger transcript understanding
* better interview-style question generation

### Note

For Hugging Face free CPU deployment, `flan-t5-base` is safer.

For stronger servers or GPU deployment, `flan-t5-large` or `flan-t5-xl` is recommended.

---

## 4. Translation Improvement

### Current Model

```text
facebook/nllb-200-distilled-600M
```

### Upgrade Options

```text
facebook/nllb-200-1.3B
facebook/nllb-200-3.3B
```

### Benefits

* more accurate multilingual translation
* better grammar
* improved native-language fluency
* stronger sentence structure

---

## 5. Production-Level Deployment Upgrade

### Current Deployment

```text
Frontend → Vercel
Backend → Hugging Face Spaces (CPU Basic)
```

### Future Upgrade Options

```text
AWS
Google Cloud
Azure
Render
Railway
GPU-based Hugging Face Spaces
```

### Benefits

* faster response time
* larger model support
* better scalability
* improved performance for real users

---

# Final Improvement Strategy

## For Free Deployment

Use:

```text
Whisper Small
BART Large CNN
FLAN-T5 Base
NLLB Distilled 600M
```

Best for:

* stability
* free hosting
* final year project demo

---

## For High Accuracy Deployment

Use:

```text
Whisper Large-v3
PEGASUS
FLAN-T5 XL
NLLB 1.3B+
```

Best for:

* research-grade output
* production systems
* startup-level deployment
* advanced AI applications

---

This makes the project flexible for both academic submission and future real-world production upgrades.

---

# Final Conclusion

This project successfully performs:

* video summarization
* transcript generation
* multilingual translation
* quiz generation

using modern NLP + Speech AI models.

It is deployment-ready, scalable, and suitable for:

* Final Year Project
* Resume Projects
* Placement Showcase
* Technical Viva Demonstration

This is the correct final production path we followed.
