# Unit Test case class to check some base conditions
# author : Harsh Verma
import unittest
import WordsCountCLIVersion

class TestCaseHandler(unittest.TestCase):
    program_doc_frequency_count = {'file1.txt': 4, 'file2.txt': 5}


    def printWordDocIDWithCount(word, word_from_docIDs_count):
            print('Word: [' + word + '] occurs in document IDs with frequency: ' + str(word_from_docIDs_count))


    def count_of_words(self, expected, word):
        list_of_selected_words = list()
        list_of_selected_words.append(word)
        word_from_docIDs_count = WordsCountCLIVersion.word_details(list_of_selected_words)
        self.assertDictEqual(word_from_docIDs_count, expected, "Result Dict is not equal")

# Test1
    def test_count_of_words(self):
        expected =  {'file1.txt': 4, 'file2.txt': 5}
        self.count_of_words(expected, "program")

# Test2
    def test_count_word_2(self):
        expected =  {'file1.txt': 8, 'file2.txt': 11, 'file3.txt': 4, 'file4.txt': 2, 'file5.txt': 2}
        self.count_of_words(expected, "the")