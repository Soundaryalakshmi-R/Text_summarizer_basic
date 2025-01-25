import pickle
from nltk.tokenize import sent_tokenize
from heapq import nlargest
from collections import Counter

# Load the pickled model
with open("nlp_model.pkl", "rb") as file:
    nlp = pickle.load(file)

def summarize_text(text, num_sentences=3):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text  # Return the full text if it's too short to summarize

    # Create a SpaCy document for NLP processing
    doc = nlp(text)

    # Calculate word frequencies (excluding stop words and punctuation)
    word_frequencies = Counter(
        token.text.lower() for token in doc if not token.is_stop and not token.is_punct
    )

    # Normalize frequencies by dividing by the maximum frequency
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sent in sentences:
        for word in sent.lower().split():
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    # Select the top N sentences with the highest scores
    summarized_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(summarized_sentences)
