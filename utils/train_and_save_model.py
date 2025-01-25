import spacy
import pickle

# Load SpaCy's language model
nlp = spacy.load("en_core_web_sm")

# Save the model to a file
with open("nlp_model.pkl", "wb") as file:
    pickle.dump(nlp, file)

print("Model saved successfully!")
