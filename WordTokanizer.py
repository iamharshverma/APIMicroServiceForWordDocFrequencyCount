# Created by - Harsh Verma
# Class to tokanize the works and get the respective count in document

# This function reads subfile and returns the words
def tokenize(filePath):
    file = open(filePath, 'r+', encoding="utf-8")
    book = file.read()
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None
    file.close()


# This function creates the map count of words and their frequency provided all the tokens as input
def map_word_count(tokens):
    hash_map = {}
    if tokens is not None:
        for element in tokens:
            for char in element:
                if not char.isalnum():
                    element = element.replace(char, "")
            word = element

            # is Word Exist
            if word in hash_map:
                hash_map[word] = hash_map[word] + 1
            else:
                hash_map[word] = 1

        return hash_map
    else:
        return None
