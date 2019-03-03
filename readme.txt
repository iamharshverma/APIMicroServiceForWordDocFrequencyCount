HP ASSESMENt BY Harsh Verma:

The program is written in python to support both CLI and HTTP API based services. The program uses python 3 or above(3.6).

The program input tested data is present in project directory under data folder with maindata.txt containing the absolute file path of sub directories and other files containing inside data folder having the conversation or usual text data

1. WordsCountCLIVersion.py : File contains the python code and takes input as command line argument of the main file.
2. WordCountsHTTPAPI.py : contains HTTP Apis for the program
3. WordTokanizer.py : Contain helper class for word map formation
4.Under test folder unit test UnitTest.py file is present which helps to get trace of some positive/negative test cases

To understand about functions and code please read the comments on top of every function, this will clear what every piece of code is doing

Command Line Execution :
To execute the program pass the main_file_path in the argument
Python WordsCountCLIVersion.py /Users/harshverma/PycharmProjects/HPWordCount/data/maindata.txt

The program will display the output of word list with frequencies across all sub files path which as provided in main file

For bonus Task execution : 
To Execute bonus task pick a word from previous word frequencies count list and enter in comma separated input words
Press enter to start execution

It will print required details of the input word/words :
Example :
Total Count for Word: [the] is: 27
Word: [the] occurs in document IDs with frequency: {'file1.txt': 8, 'file2.txt': 11, 'file3.txt': 4, 'file4.txt': 2, 'file5.txt': 2}
Word: [the] occurs in full document Path with frequency: {'/Users/harshverma/PycharmProjects/HPWordCount/data/file1.txt': 8, '/Users/harshverma/PycharmProjects/HPWordCount/data/file2.txt': 11, '/Users/harshverma/PycharmProjects/HPWordCount/data/file3.txt': 4, '/Users/harshverma/PycharmProjects/HPWordCount/data/file4.txt': 2, '/Users/harshverma/PycharmProjects/HPWordCount/data/file5.txt': 2}



2. WordCountsHTTPAPI.py : File contains the code written to support the services via HTTP API.
It uses flask to support the HTTP API wrapper .

To start the execution run file :
python3.6 WordCountsHTTPAPI.py

-> This will start the python flask server and will listen to the request HTTP request in Running on http://0.0.0.0:7000/ (Press CTRL+C to quit) host and port.

Hit the Curl call using postman or terminal to make a HTTP post call 
1. For Displaying word count :
Example curl for displaying word list with frequencies :
 -> Provide the key parameter as "main_file_path" to give main file full path

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt"}' http://0.0.0.0:7000/priority-words/get

2. For Displaying details of given word as input(Bonus Task) :
Maintain the key parameters in curl call :
I) main_file_path : Provide the key parameter as "main_file_path" to give main file full path
ii) word_list : provide input word in list to get the details associated with it
iii) If you want to print full path of sub directory file in which the word is stored use key ->
is_full_document_path_needed : True 
This will provide full paths where the word is present along with its document frequency

Curl1 : curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt" , "word_list" : ["program"] , "is_full_document_path_needed" : "False"}' http://0.0.0.0:7000/words-count/get


For getting information about multiple words in a go : provide input words in list as comma separated under key "word_list"

Curl2 : curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"main_file_path": "/Users/harshverma/Documents/Project_repo/HPProject/maindata.txt" , "word_list" : ["program", "true"] , "is_full_document_path_needed" : "False"}' http://0.0.0.0:7000/words-count/get



Thanks for reading this basic version of doc please do read ProgramDocExecutionAndOutput.pdf or ProgramDocExecutionAndOutput.docx for more details and sample input outputs 





