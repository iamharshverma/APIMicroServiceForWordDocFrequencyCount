import os
import WordTokanizer
import sys

# Declaring global dict to be used in program
# docToWordsCount : This will store key as docID and value as map of word with frequency
# docID_to_absolute_filepath_dict : This stores key as docID i.e filename and value as full absolute path of file,
# just in case if we want to display full file name with path(Its a extra feature which can be handled via api call parameter is_full_filepath_needed)
# super_words_dict : Dict containing all words with frequencies across all files

doc_to_words_count = {}
docID_to_absolute_filepath_dict = {}
super_words_dict = {}
docId_wordCount_map = {}

## Function to process and tokanize each work in given sub filepath
def process_file(subfilePath, docId):
    tokanized_words = WordTokanizer.tokenize(subfilePath)
    mapWords = WordTokanizer.map_word_count(tokanized_words)
    doc_to_words_count[docId] = mapWords
    return doc_to_words_count

# Function to print word count from various document id and their frequency in each doc
def print_wordDocID_with_count(word, word_from_docIDs_count, is_full_document_path_needed):
    if (is_full_document_path_needed):
        tmp_docpath_frequency_dict = {}
        for key, value in word_from_docIDs_count.items():
            key = docID_to_absolute_filepath_dict.get(key)
            tmp_docpath_frequency_dict[key] = value

        print('Word: [' + word + '] occurs in full document Path with frequency: ' + str(tmp_docpath_frequency_dict))
        print("\n")

    else:
        print('Word: [' + word + '] occurs in document IDs with frequency: ' + str(word_from_docIDs_count))


# Helper Function to print total word count of a given word across all files
def print_totalCount_for_word(word, total_count):
    print('Total Count for Word: [' + word + '] is: ' + str(total_count))


# Handles Bonus Conditions which was asked in question
# Helper function to provide given list of words as input details , I.e 1. whats the total count of that word across all files, 2. Whats the count with respect to each files with documnet id
def word_details(list_of_selected_words):
    for word in list_of_selected_words:
        word_from_docIDs_count = {}
        total_count = super_words_dict.get(word)
        print_totalCount_for_word(word, total_count)
        for docID, valueCountMap in docId_wordCount_map.items():
            if (valueCountMap.get(word) is not None):
                count = valueCountMap.get(word)
                word_from_docIDs_count[docID] = count
        print_wordDocID_with_count(word, word_from_docIDs_count, False)
        print_wordDocID_with_count(word, word_from_docIDs_count, True)
    return word_from_docIDs_count


## Main Program execution start here
try:
    main_file_path = sys.argv[1]
except:
    dir = os.path.dirname(__file__)
    main_file_path = os.path.join(dir, 'data' ,'maindata.txt')

# Main Code to Start Program execution and read main data file
mainFile = open(main_file_path, "r")


for aline in mainFile:
    aline = aline.strip();
    filePathSplit = os.path.normpath(aline)
    fileSplitArray = filePathSplit.split(os.sep)
    docId = fileSplitArray[-1]
    docID_to_absolute_filepath_dict[docId] = aline
    docId_wordCount_map = process_file(aline, docId)

# Loop to store Map i.e key as doc id with respect to word-count Map as value
for k, v in docId_wordCount_map.items():
    wordCountMap = v
    for wordKey, count in wordCountMap.items():
        if super_words_dict.get(wordKey) is None:
            super_words_dict[wordKey] = count

        else:
            curr_count = super_words_dict.get(wordKey)
            curr_count = curr_count + count
            super_words_dict[wordKey] = curr_count

# Creating a super dic of words with overall frequency and displaying it
print("\n")
print("Displaying Super words Dict with frequencies:")
print("\n")
print(super_words_dict)
print("\n")
mainFile.close()
# list_of_selected_words : This stores the input word list for that the detailed information needs to be traced


list_of_selected_words = list()
try:
    var = input("Provide the input list of words for which detail is required, if only one word then enter input_word else for multiple inputs enter comma separated words")
    print("\n")
    input_var = str(var)
    print("\n")
    print("You entered " + input_var)
    if(',' in input_var):
        input_words = input_var.split(",")
        for word in input_words:
            list_of_selected_words.append(word)

    else:
        list_of_selected_words.append(input_var)
    word_details(list_of_selected_words)
except:
    raise Exception("Provide the input list of words for which detail is required in given format: if only one word then enter input_word else for multiple inputs enter comma separated words")

# Sample example for word : program and the as input to get their total count and document , frequency count
# Function call to process list of input
