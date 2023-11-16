

def read_files():
    
    line_id_to_text = {}
    
    with open("movies_lines.txt", errors="ignore") as movie_lines:
        data = movie_lines.readlines()
        
    for line in data:
        sequences = line.replace("\n", "").split(" +++$+++ ")
        line_id_index = 0
        sentence_index = 4
        line_id_to_text[sequences[line_id_index]] = sequences[sentence_index]

