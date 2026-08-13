# Dev Voice Assistant — "Nova"

A voice-controlled assistant that opens the tools students use every day
just by asking: Google Colab, GitHub, code.org, and VS Code — plus jokes,
motivational quotes, time, and date, for a bit of personality.

## Setup

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

2. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

   **If `pyaudio` fails to install (common on Windows):**
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

3. (Optional, for "open vs code" to work) Make sure the `code` command is
   available in your terminal. In VS Code: `Ctrl+Shift+P` → type
   **"Shell Command: Install 'code' command in PATH"** → run it. Restart
   the terminal afterward.

## Run it

```bash
python main.py
```

## Example commands to try
| Say this | It does this |
|---|---|
| "open colab" | opens Google Colab in your browser |
| "open github" | opens GitHub |
| "open code dot org" | opens code.org |
| "open vs code" | launches VS Code in the current folder |
| "open chatgpt" | opens ChatGPT |
| "open kaggle" | opens Kaggle |
| "open stack overflow" | opens Stack Overflow |
| "search youtube for neural networks" | searches YouTube for that topic |
| "search google for transformers" | searches Google for that topic |
| "what is machine learning" | Nova explains ML in one sentence |
| "what is nlp" | Nova explains NLP |
| "what is computer vision" | Nova explains computer vision |
| "what is generative ai" | Nova explains generative AI |
| "what is a neural network" | Nova explains neural networks |
| "what is overfitting" | Nova explains overfitting |
| "what is prompt engineering" | Nova explains prompt engineering |
| "hello" / "hi" | Nova greets you back |
| "how are you" | Nova chats back |
| "what can you do" | Nova lists everything it can do |
| "tell me a joke" | Nova tells a programming joke |
| "motivate me" | Nova shares a coding quote |
| "what time is it" | tells the current time |
| "stop" / "exit" | shuts down |

## Why it used to stop after one command
The earlier version reused a single `pyttsx3` speech engine across the
whole session, which can silently freeze on some Windows setups after
the first response. This version creates a **fresh engine every time it
speaks**, and the whole listening loop is wrapped in error handling so
one bad response can never kill the assistant — it just logs the error
and keeps listening.

## Adding your own bootcamp Q&A
Open `main.py` and find `KNOWLEDGE_BASE` near the top — it's a simple
list of `(keyword, spoken answer)` pairs. Add a new line in the same
format to teach Nova a new topic, e.g.:
```python
("supervised learning", "Supervised learning is when a model learns from "
                         "labeled data, where each example has a known answer."),
```

## Classroom "wow moment" ideas
- Have every student say **"open colab"** at the same time and watch 20
  browser tabs pop open across the room simultaneously.
- Let students add their own command in `handle_command()` — a great
  mini-challenge (e.g., "open WhatsApp Web", "open ChatGPT", "tell me a
  fun fact").
- Change `ASSISTANT_NAME` to something the class votes on together.

## Common issues
| Problem | Fix |
|---|---|
| `pyaudio` won't install | use `pipwin install pyaudio` (Windows) |
| "open vs code" doesn't launch | `code` command isn't in PATH — see setup step 3 |
| Assistant mishears commands | speak clearly, reduce background noise; `adjust_for_ambient_noise` already helps |
| No internet = no recognition | Google's speech API needs an internet connection |
