from nltk.tokenize import sent_tokenize
from heapq import nlargest

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    word_frequencies = {}
    for word in text.split():
        word = word.lower()
        word_frequencies[word] = word_frequencies.get(word, 0) + 1
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq
    sentence_scores = {sent: sum(word_frequencies.get(word.lower(), 0) for word in sent.split()) for sent in sentences}
    summary = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(summary)
