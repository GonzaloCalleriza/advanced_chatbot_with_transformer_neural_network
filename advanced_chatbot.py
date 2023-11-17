import re
import tensorflow_datasets as tfds
import tensorflow as tf

# Process the data from the two text files
def read_files():
    
    line_id_to_text = {}
    
    with open("movies_lines.txt", errors="ignore") as movie_lines:
        data = movie_lines.readlines()
        
    for line in data:
        sequences = line.replace("\n", "").split(" +++$+++ ")
        line_id_index = 0
        sentence_index = 4
        line_id_to_text[sequences[line_id_index]] = sequences[sentence_index]
        
    return line_id_to_text

line_id_to_text = read_files()

def read_conversations():
    
    inputs, outputs = [], []
    
    with open("movie_conversations.txt", errors="ignore") as conversations:
        data = conversations.readlines()
    for line in data:
        sequences = line.replace("\n", "").split(" +++$+++ ")
        conversation = [line[1:-1] for line in sequences[3][1:-1].split(", ")]
        
        for index in range(len(conversation) - 1):
            inputs.append(line_id_to_text[conversation[index]])
            outputs.append(line_id_to_text[conversation[index + 1]])
            
            if len(inputs) >= 100000:
                return inputs, outputs
            
    return inputs, outputs

inputs, outputs = read_conversations()

# Clean data for NLP
def clean_text(sentence):
    lowercase = sentence.lower()
    stripped_whitespace = lowercase.strip()
    
    new_sentence = re.sub(r"([?.!,])", r"\1", stripped_whitespace)
    new_sentence = re.sub(r'[" "]+', " ", new_sentence)
    
    return new_sentence

# Removing contractions

def remove_contractions(sentence):
    sentence = re.sub(r"we'd", "we would", sentence)
    sentence = re.sub(r"that's", "that is", sentence)
    sentence = re.sub(r"you're", "you are", sentence)
    sentence = re.sub(r"what's", "what is", sentence)
    sentence = re.sub(r"it's", "it is", sentence)
    sentence = re.sub(r"didn't", "did not", sentence)
    sentence = re.sub(r"i'm", "i am", sentence)
    sentence = re.sub(r"can't", "can not", sentence)
    sentence = re.sub(r"\'d", " would", sentence)
    sentence = re.sub(r"\'ll", " will", sentence)
    sentence = re.sub(r"\'re", " are", sentence)
    sentence = re.sub(r"\'ve", " have", sentence)
    
# Preprocess text data for Transformer chatbot ML
def preprocess_text(data):
    processed_data = []
    for sentence in data:
        cleaned = clean_text(sentence)
        new_sentence = remove_contractions(cleaned)
        
        new_sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", new_sentence)
        stripped_sentence = new_sentence.strip()
        processed_data.append(stripped_sentence)
        
    return processed_data

cleaned_inputs = preprocess_text(inputs)
cleaned_outputs = preprocess_text(outputs)

# Build a tokenizer with tfds

tokenizer = tfds.deprecated.text.SubwordTextEncoder.build_from_corpus(
    cleaned_inputs + cleaned_outputs,
    target_vocab_size = 2**10
)

start_token = [tokenizer.vocab_size]
end_token = [tokenizer.vocab_size + 1]

def tokenize(inputs, outputs):
    
    tokenized_inputs, tokenized_outputs = [], []
    
    for(question, answer) in zip(inputs, outputs):
        question = start_token + tokenizer.encode(question) + end_token
        answer   = start_token + tokenizer.encode(answer)   + end_token
        
        tokenized_inputs.append(question)
        tokenized_outputs.append(answer)
    
    return tokenized_inputs, tokenized_outputs

tokenized_inputs, tokenized_outputs = tokenize(cleaned_inputs, cleaned_outputs)

# Adding padding to tokenized sentences with Python
padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
    tokenized_inputs, padding="post"
)

padded_outputs = tf.keras.preprocessing.sequence.pad_sequences(
    tokenized_outputs, padding="post"
)