

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