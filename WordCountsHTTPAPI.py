## Created by Harsh Verma
# Used Import
import os
import WordTokanizer
from flask import Flask, request
from flask import jsonify
app = Flask(__name__)

# Global variable  to store filename with respect to file full path as value
docID_to_absolute_filepath_dict = {}

## Helper Function to process and tokanize each work in given sub filepath
def process_file(subfilePath):
    tokanized_words = WordTokanizer.tokenize(subfilePath)
    map_words = WordTokanizer.map_word_count(tokanized_words)
    return map_words

# Helper function to provide super_words_dict which is super set of words and its frequency across all files
## Input docId_word_frequency_count_map : document id as key , <word,frequency> as map value
## Input super_words_dict :Global Dict of super words
## returns super_words_dict
def provide_superset_words(docId_word_frequency_count_map, super_words_dict):
    for k, v in docId_word_frequency_count_map.items():
        word_count_map = v
        for wordKey, count in word_count_map.items():
            if super_words_dict.get(wordKey) is None:
                super_words_dict[wordKey] = count

            else:
                curr_count = super_words_dict.get(wordKey)
                curr_count = curr_count + count
                super_words_dict[wordKey] = curr_count

    return super_words_dict

# Helper function to process words in superset and display word frequency
# Takes input as main file path which is provided by API input via parameter "main_file_path"
# Returns the super word dict of all element with frequncy across all files and document id to word count map
def process_superset_words(main_file_path):
    main_file = open(main_file_path, "r")
    super_words_dict = {}
    doc_id_to_word_count_map = {}
    for aline in main_file:
        aline = aline.strip();
        file_path_split = os.path.normpath(aline)
        file_split_array = file_path_split.split(os.sep)
        docId = file_split_array[-1]
        docID_to_absolute_filepath_dict[docId] = aline
        doc_id_to_word_count_map[docId] = process_file(aline)
    super_words_dict = provide_superset_words(doc_id_to_word_count_map, super_words_dict)
    main_file.close()
    return super_words_dict , doc_id_to_word_count_map


# Sample curl call : curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt"}' http://0.0.0.0:7000/priority-words/get
# API to fetch all words list across all sub-directories of a main_file_path
# Takes input as API parameter post call with key as main_file_path
# returns the data(words with their frequencies) in json format in http request body with key d

@app.route('/priority-words/get', methods=['POST'])
def process_and_provide_words_with_frequencies():
    if request.method == 'POST':
        data="False"
        # If all good return HTTP code : 200 with data
        try:
            main_file_path = request.get_json().get("main_file_path")
            data = process_superset_words(main_file_path)
            resp = jsonify(**{'d': dict(data=data)})
            resp.status_code = 200

        # If error occured return HTTP code : 500 with data as False and logger displaying the issue
        except Exception as e:
            resp = jsonify(**{'d': dict(data=data)})
            resp.status_code = 500

        return resp

# Function to print word count from various document id and their frequency in each doc
def print_wordDocID_with_count(word, word_from_docIDs_count, is_full_document_path_needed):
    if (is_full_document_path_needed):
        tmp_docpath_frequency_dict = {}
        for key, value in word_from_docIDs_count.items():
            key = docID_to_absolute_filepath_dict.get(key)
            tmp_docpath_frequency_dict[key] = value

        print('Word: [' + word + '] occurs in document Path with frequency: ' + str(tmp_docpath_frequency_dict))

    else:
        print('Word: [' + word + '] occurs in document IDs with frequency: ' + str(word_from_docIDs_count))

# Helper Function to print total word count of a given word across all files
def printTotalCountForWord(word, total_count):
    print('Total Count for Word: [' + word + '] is: ' + str(total_count))
    print("\n")

# API 2 Helper Function to display the word details which is asked in bonus task i.e
# I.e 1. whats the total count of that word across all files, 2. Whats the count with respect to each files with documnet id

def word_details(list_of_selected_words, super_words_dict, is_full_document_path_needed, docId_words_count_map):
    combined_word_from_docIDs_count = {}
    for word in list_of_selected_words:
        total_count = 0
        print("Word is ", word)
        word_from_docIDs_count = {}
        total_count = super_words_dict.get(word)
        printTotalCountForWord(word, total_count)

        for doc_id, value_count_map in docId_words_count_map.items():
            if (value_count_map.get(word) is not None):
                count = value_count_map.get(word)
                if(is_full_document_path_needed):
                    doc_id = docID_to_absolute_filepath_dict.get(doc_id)

                word_from_docIDs_count[doc_id] = count

        # Can uncomment this for printing the result on API console
        #printWordDocIDWithCount(word, word_from_docIDs_count, False)
        #printWordDocIDWithCount(word, word_from_docIDs_count, True)
        combined_word_from_docIDs_count["word : "+ word] = [word_from_docIDs_count, "total:" + str(total_count)]

    return combined_word_from_docIDs_count


# Sample curl call 2: curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt" , "word_list" : ["program"] , "is_full_document_path_needed" : "False"}' http://0.0.0.0:7000/words-count/get
# Sample curl call 2 with multiple input : curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt" , "word_list" : ["program", "the"] , "is_full_document_path_needed" : "False"}' http://0.0.0.0:7000/words-count/get
# Sample curl call 3 to display full path of files: curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt" , "word_list" : ["program"] , "is_full_document_path_needed" : "True"}' http://0.0.0.0:7000/words-count/get
#
# API to display details of input words (Bonus Task Detail)
# Takes input as API parameter post call with key as main_file_path : Provide main file full path , word_list : provide the list of input words for which details needs
# to be traced , is_file_full_path_needed : if (True) : manages if full document path is needed to be displayed ,else(False) : just document name
# returns the data(words with their frequencies) in json format in http request body with key d

# Sample output : {"d":{"data":{"word : program":[{"file1.txt":4,"file2.txt":5},"total:9"],"word : the":[{"file1.txt":8,"file2.txt":11,"file3.txt":4,"file4.txt":2,"file5.txt":2},"total:27"]}}}
@app.route('/words-count/get', methods=['POST'])
def provide_wordcount_with_frequencies_and_docID():
    if request.method == 'POST':
        data="False"

        try:
            main_path = request.get_json().get("main_file_path")
            super_words_dict, docIdJsonMap = process_superset_words(main_path)
            print("Inside API: ", docIdJsonMap)
            word_list = request.get_json().get("word_list")
            is_full_document_path_needed = request.get_json().get("is_file_full_path_needed")
            if(is_full_document_path_needed is None):
                is_full_document_path_needed = False
            data = word_details(word_list, super_words_dict, is_full_document_path_needed, docIdJsonMap)
            resp = jsonify(**{'d': dict(data=data)})
            resp.status_code = 200

        except Exception as e:
            resp = jsonify(**{'d': dict(data=data)})
            resp.status_code = 500

        return resp

# Starting main flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, threaded=True)