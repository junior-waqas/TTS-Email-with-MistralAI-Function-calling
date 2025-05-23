# 📨 Voice-to-Email Assistant using Whisper and Mistral AI

This Python project converts a **voice note to text** using OpenAI's Whisper model, then uses **Mistral AI** to interpret the message and **automatically send an email** via Gmail based on the transcribed content.

---

## 🔧 Features

- 🎙️ Transcribes voice notes using `whisper`.
- 🧠 Uses Mistral AI to interpret intent from user speech.
- 📧 Sends emails automatically via Gmail SMTP.
- 🔐 Secures credentials using environment variables (`.env`).

---

## 📦 Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
