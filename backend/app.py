# Main backend for AI Video Summarizer + Quiz Generator

from flask import Flask, request, jsonify
import os
import math
import random
import ffmpeg
import whisper
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Folder setup

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Home route

@app.route("/")
def home():
    return "AI Video Summarizer Backend Running"


# Upload and process route

@app.route("/upload", methods=["POST"])
def upload_video():

    # Basic file validation

    if "video" not in request.files:
        return jsonify({
            "error": "No video file provided"
        }), 400

    file = request.files["video"]

    if file.filename == "":
        return jsonify({
            "error": "Empty filename"
        }), 400

    # Save uploaded video

    video_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(video_path)

    audio_path = os.path.join(
        OUTPUT_FOLDER,
        "audio.wav"
    )

    try:

        # Step 1: Extract audio from video

        (
            ffmpeg
            .input(video_path)
            .output(audio_path)
            .run(overwrite_output=True)
        )

        # Step 2: Convert speech to text using Whisper

        whisper_model = whisper.load_model("small")

        result = whisper_model.transcribe(audio_path)
        transcript = result["text"]

        transcript_path = os.path.join(
            OUTPUT_FOLDER,
            "transcript.txt"
        )

        with open(
            transcript_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(transcript)

        # Step 3: Generate summary using BART

        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

        summary_result = summarizer(
            transcript[:1500],
            max_length=200,
            min_length=80,
            do_sample=False
        )

        summary = summary_result[0]["summary_text"]

        summary_path = os.path.join(
            OUTPUT_FOLDER,
            "summary.txt"
        )

        with open(
            summary_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(summary)

        # Step 4: Quiz generation using FLAN-T5
        # FLAN-T5 works better when generating one Q&A at a time

        quiz_generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-large"
        )

        # Get video duration

        probe = ffmpeg.probe(video_path)
        duration_seconds = float(
            probe["format"]["duration"]
        )
        duration_minutes = duration_seconds / 60

        # Around 2 questions per minute
        # minimum 3 and maximum 10

        num_questions = min(
            10,
            max(3, math.ceil(duration_minutes * 2))
        )

        print(f"\nVideo Duration: {duration_minutes:.1f} minutes")
        print(f"Generating {num_questions} quiz questions...\n")

        # Split transcript into chunks

        words = transcript.split()
        total_words = len(words)
        chunk_size = max(1, total_words // num_questions)

        quiz_data = []
        generated_questions = set()
        all_correct_answers = []

        for i in range(num_questions):

            start_idx = i * chunk_size
            end_idx = min(
                start_idx + chunk_size + 20,
                total_words
            )

            chunk = " ".join(words[start_idx:end_idx])

            # Keep chunk small for FLAN-T5 token limits
            chunk = chunk[:400]

            # Generate question

            q_prompt = (
                f"Read the following text and generate one meaningful question based on it.\n\n"
                f"Text: {chunk}\n\n"
                f"Question:"
            )

            q_result = quiz_generator(
                q_prompt,
                max_new_tokens=64,
                do_sample=False
            )

            question = q_result[0]["generated_text"].strip()

            if question.lower() in generated_questions or not question.endswith("?"):
                continue

            generated_questions.add(question.lower())

            # Generate short answer

            a_prompt = (
                f"Based on the text, answer this question as briefly as possible (1-5 words).\n\n"
                f"Text: {chunk}\n"
                f"Question: {question}\n\n"
                f"Answer:"
            )

            a_result = quiz_generator(
                a_prompt,
                max_new_tokens=32,
                do_sample=False
            )

            correct_answer = a_result[0]["generated_text"].strip()

            if correct_answer:
                quiz_data.append({
                    "question": question,
                    "correct": correct_answer
                })

                if correct_answer.lower() not in [
                    ans.lower() for ans in all_correct_answers
                ]:
                    all_correct_answers.append(correct_answer)

        # Build MCQ options

        quiz_lines = []

        fallback_distractors = [
            "All of the above",
            "None of the above",
            "Information not provided",
            "Not enough context"
        ]

        for idx, item in enumerate(quiz_data):
            q_num = idx + 1
            question = item["question"]
            correct_answer = item["correct"]

            distractors = [
                ans for ans in all_correct_answers
                if ans.lower() != correct_answer.lower()
            ]

            options = [correct_answer]

            if len(distractors) >= 2:
                options.extend(random.sample(distractors, 2))
            elif len(distractors) == 1:
                options.append(distractors[0])
                options.append(random.choice(fallback_distractors))
            else:
                options.extend(random.sample(fallback_distractors, 2))

            random.shuffle(options)

            correct_letter = ""
            formatted_options = []
            labels = ["A", "B", "C"]

            for i, opt in enumerate(options):
                formatted_options.append(f"{labels[i]}) {opt}")

                if opt == correct_answer:
                    correct_letter = labels[i]

            mcq_text = (
                f"{question}\n"
                f"{formatted_options[0]}\n"
                f"{formatted_options[1]}\n"
                f"{formatted_options[2]}\n"
                f"Correct Answer: {correct_letter}"
            )

            formatted_mcq = f"Q{q_num}: {mcq_text}"
            quiz_lines.append(formatted_mcq)

            print(f"--- Question {q_num} ---\n{mcq_text}\n")

        quiz_text = "\n\n".join(quiz_lines)

        print("\n==============================")
        print("QUIZ OUTPUT")
        print("==============================")
        print(quiz_text)
        print("==============================\n")

        quiz_path = os.path.join(
            OUTPUT_FOLDER,
            "quiz.txt"
        )

        with open(
            quiz_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(quiz_text)

        # Step 5: Language selection

        language_map = {
            "Telugu": "tel_Telu",
            "Hindi": "hin_Deva",
            "Tamil": "tam_Taml",
            "Kannada": "kan_Knda",
            "Malayalam": "mal_Mlym",
            "English": "eng_Latn"
        }

        selected_language = request.form.get(
            "language",
            "Telugu"
        )

        target_language_code = language_map.get(
            selected_language,
            "tel_Telu"
        )

        # Step 6: Translation using NLLB

        translator = pipeline(
            "translation",
            model="facebook/nllb-200-distilled-600M"
        )

        translated_transcript_result = translator(
            transcript[:2000],
            src_lang="eng_Latn",
            tgt_lang=target_language_code,
            max_length=800
        )

        translated_transcript = (
            translated_transcript_result[0]["translation_text"]
        )

        translated_transcript_path = os.path.join(
            OUTPUT_FOLDER,
            "translated_transcript.txt"
        )

        with open(
            translated_transcript_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(translated_transcript)

        translated_summary_result = translator(
            summary,
            src_lang="eng_Latn",
            tgt_lang=target_language_code,
            max_length=400
        )

        translated_summary = (
            translated_summary_result[0]["translation_text"]
        )

        translated_summary_path = os.path.join(
            OUTPUT_FOLDER,
            "translated_summary.txt"
        )

        with open(
            translated_summary_path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(translated_summary)

        # Final API response

        return jsonify({
            "message": "Video uploaded, transcript, summary, quiz, and translation generated successfully",

            "selected_language": selected_language,

            "video_path": video_path,
            "audio_path": audio_path,

            "transcript_path": transcript_path,
            "translated_transcript_path": translated_transcript_path,

            "summary_path": summary_path,
            "translated_summary_path": translated_summary_path,

            "quiz_path": quiz_path,

            "transcript_preview": transcript[:500] + (
                "..." if len(transcript) > 500 else ""
            ),
            "summary_preview": summary,
            "quiz_preview": quiz_text,
            "translated_summary_preview": translated_summary
        })

    except Exception as e:
        print("FULL ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


# Run Flask app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)