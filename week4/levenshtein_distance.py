import streamlit as st
import os

def levenshtein_distance(token1, token2):
    """
    Calculates the Levenshtein distance between two input tokens.

    Parameters:
    token1 (str): The first token.
    token2 (str): The second token.

    Returns:
    int: The Levenshtein distance between the two tokens.
    """
    len_t1, len_t2 = len(token1), len(token2)
    distances = [[0] * (len_t2 + 1) for _ in range(len_t1 + 1)]

    for t1 in range(len_t1 + 1):
        distances[t1][0] = t1

    for t2 in range(len_t2 + 1):
        distances[0][t2] = t2

    for t1 in range(1, len_t1 + 1):
        for t2 in range(1, len_t2 + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                distances[t1][t2] = min(
                    distances[t1][t2 - 1] + 1,    # Insertion
                    distances[t1 - 1][t2] + 1,    # Deletion
                    distances[t1 - 1][t2 - 1] + 1 # Substitution
                )

    return distances[len_t1][len_t2]

def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words
vocabs = load_vocab(file_path=f'{os.path.dirname(os.path.realpath(__file__))}/data/vocab.txt')

def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):

        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)
        
        # sorted by distance
        sorted_distences = dict(sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)
        
        col2.write('Distances:')
        col2.write(sorted_distences)

if __name__ == "__main__":
    main()