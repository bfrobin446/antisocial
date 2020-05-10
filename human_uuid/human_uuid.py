from pathlib import Path

BITS_PER_WORD = 12
_MASK = (1 << BITS_PER_WORD) - 1

module_dir = Path(__file__).parent
with open(module_dir / 'words.txt') as words_file:
    _WORDS = [line.strip() for line in words_file]

assert len(_WORDS) == 2**BITS_PER_WORD

def encode(uuid, n_words=10):
    selected_words = []
    for i in range(128-BITS_PER_WORD, 0, -BITS_PER_WORD):
        word_index = (uuid.int >> i) & _MASK
        selected_words.append(_WORDS[word_index])
    return '-'.join(selected_words[:n_words])
