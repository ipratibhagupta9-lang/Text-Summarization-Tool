import tkinter as tk
from tkinter import ttk, messagebox
import re

# ============================================================
# STOPWORDS
# ============================================================

STOPWORDS = set("""
a about above after again against all am an and any are as at be
because been before being below between both but by can cannot could
did do does doing down during each few for from further had has have
having he her here hers herself him himself his how i if in into is
it its itself me more most my myself no nor not of off on once only
or other our ours ourselves out over own same she should so some
such than that the their theirs them themselves then there these
they this those through to too under until up very was we were what
when where which while who whom why with would you your yours
yourself yourselves also said say says one two used use
""".split())


# ============================================================
# NLP FUNCTIONS
# ============================================================

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def sentence_tokenize(text):
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def word_tokenize(text):
    return re.findall(r"[a-zA-Z']+", text.lower())


def build_word_frequencies(words):
    freq = {}

    for word in words:
        if word in STOPWORDS or len(word) <= 1:
            continue

        freq[word] = freq.get(word, 0) + 1

    if not freq:
        return {}

    max_freq = max(freq.values())

    for word in freq:
        freq[word] /= max_freq

    return freq


def score_sentences(sentences, word_freq):
    scores = []

    for sent in sentences:
        words = word_tokenize(sent)

        important_words = [w for w in words if w in word_freq]

        if not important_words:
            scores.append(0)
            continue

        score = sum(word_freq[w] for w in important_words)
        score /= len(important_words)

        scores.append(score)

    return scores


def summarize(text, ratio=0.3):
    sentences = sentence_tokenize(text)

    if not sentences:
        return "", {}

    words = word_tokenize(text)
    word_freq = build_word_frequencies(words)
    scores = score_sentences(sentences, word_freq)

    n = max(1, round(len(sentences) * ratio))

    ranked = sorted(
        range(len(sentences)),
        key=lambda i: scores[i],
        reverse=True
    )

    selected = sorted(ranked[:n])

    summary = " ".join(sentences[i] for i in selected)

    stats = {
        "Original Sentences": len(sentences),
        "Summary Sentences": len(selected),
        "Original Words": len(words),
        "Summary Words": len(word_tokenize(summary))
    }

    return summary, stats


# ============================================================
# GUI FUNCTIONS
# ============================================================

def generate_summary():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    ratio = ratio_var.get() / 100

    summary, stats = summarize(text, ratio)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, summary)

    stats_label.config(
        text=
        f"Original Sentences: {stats['Original Sentences']}\n"
        f"Summary Sentences: {stats['Summary Sentences']}\n"
        f"Original Words: {stats['Original Words']}\n"
        f"Summary Words: {stats['Summary Words']}"
    )


def copy_summary():
    summary = output_text.get("1.0", tk.END)

    root.clipboard_clear()
    root.clipboard_append(summary)

    messagebox.showinfo("Copied", "Summary copied to clipboard.")


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Text Summarization Tool")
root.geometry("1000x700")

title = tk.Label(
    root,
    text="Text Summarization Tool",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

# Input Frame

tk.Label(root, text="Enter Text:", font=("Arial", 12, "bold")).pack()

input_text = tk.Text(root, height=12, width=120)
input_text.pack(padx=10, pady=5)

# Summary Length

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(
    frame,
    text="Summary Length (%)"
).pack(side=tk.LEFT)

ratio_var = tk.IntVar(value=30)

ratio_slider = ttk.Scale(
    frame,
    from_=10,
    to=100,
    orient="horizontal",
    variable=ratio_var
)

ratio_slider.pack(side=tk.LEFT, padx=10)

# Buttons

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

generate_btn = tk.Button(
    btn_frame,
    text="Generate Summary",
    command=generate_summary,
    width=20
)

generate_btn.pack(side=tk.LEFT, padx=10)

copy_btn = tk.Button(
    btn_frame,
    text="Copy Summary",
    command=copy_summary,
    width=20
)

copy_btn.pack(side=tk.LEFT)

# Output

tk.Label(
    root,
    text="Summary:",
    font=("Arial", 12, "bold")
).pack()

output_text = tk.Text(root, height=10, width=120)
output_text.pack(padx=10, pady=5)

# Stats

stats_label = tk.Label(
    root,
    text="Statistics will appear here",
    font=("Arial", 11),
    justify="left"
)

stats_label.pack(pady=10)

root.mainloop()
