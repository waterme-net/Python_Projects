# Uncomment the following lines if you run the optional run_file tests locally
# so the input shows up in the output file. Do not copy these lines into Codio.
#
# import sys
# def input( prompt=None ):
#    if prompt != None:
#        print( prompt, end="" )
#    aaa_str = sys.stdin.readline()
#    aaa_str = aaa_str.rstrip( "\n" )
#    print( aaa_str )
#    return aaa_str

import csv
import string
from operator import itemgetter


def open_file(message):
    '''
    runs a for loop checking if the file can be opened or not, if it can not be then it prompts a error message
    Argument: meesage (string)
    returns: open file
    '''
    while True:
        try:
            file_name_input = input(f'\nEnter a filename for the {message}: ')
            file_object = open(file_name_input, "r")
            return file_object

        except FileNotFoundError:
            print('\nError in words!')


def read_stopwords(fp):
    '''
    initialises an empty list, then runs a for loop taking the file opened as an input,
    makes a list of words from each line and then runs another loop for the words in the list,
    it removes the punctuation, whitespace, makes them lower character and adds them to the empty list initialised at the start
    it then makes that list into a set
    closes the file and returns the set
    Arguments: fp (open file)
    returns: set
    '''
    list = []

    for line in fp:
        word_list = line.split()

        for word in word_list:
            word = word.strip().strip(string.punctuation)
            word.lower()
            list.append(word)
    set_1 = set(list)
    fp.close()
    return set_1


def validate_word(word, stopwords):
    '''
    takes two arguments
    makes the word in the argument into small characters
    then it will check if the word is containing only letter and the word is not in stopwords
    arugments: word, stopwords
    returns: True/False
    '''
    word = word.lower()
    return word.isalpha() and word not in stopwords


def process_lyrics(lyrics, stopwords):
    '''
    Arguments: lyrics, stopwords
    makes an empty list,
    then makes a list of words from the argument lyrics
    runs a for loop checking each word in the lyric
        removes the white space, punctuation and also makes the charcters small
        checks if the word is valid
            if it the word is valid it will append it to the empty list at the start
    makes the empty list a set
    returns the set
    Returns: set
    '''
    list_2 = []

    lyrics_list = lyrics.split()
    for lyric_word in lyrics_list:
        lyric_word = lyric_word.strip().strip(string.punctuation)
        lyric_word = lyric_word.lower()

        if validate_word(lyric_word, stopwords) == True:
            list_2.append(lyric_word)
    set_2 = set(list_2)
    return set_2


def update_dictionary(data_dict, singer, song, words):
    '''
    Arguemnts: data_dict(dictionary), singer(string), song(string), words(string)
    makes an empty dictionary
    checks if the singer is in the dictionary provided in the arguement
        if it is then it adds the singer to song_dict
    it then add song and word in song_dict as key and value respectively
    then adds singer and song_dict to data_dict as key and value respectively
    doesnt return anything
    '''
    song_dict = {}
    if (singer in data_dict):
        song_dict = data_dict[singer]

    (key, val) = song, words
    song_dict[key] = (val)

    (key, val) = singer, song_dict
    data_dict[key] = (val)


def read_data(fp, stopwords):
    '''
    Arguments: fp(file), stopwords(string)
    read the file
    skips the header
    makes an empty dictionary
    runs a for loop for the lines in the file
        makes three variables and gives them value of each row while making the third row in lowercase
        puts the data through the processing_lyrics function and later in the update_dictionary function

    closes the file
    returns the dictionary
    '''

    reader = csv.reader(fp)
    next(reader)
    data_dict = {}

    for row in reader:
        coloumn_0 = row[0]
        coloumn_1 = row[1]
        coloumn_2 = row[2].lower()

        processing = process_lyrics(coloumn_2, stopwords)

        update_dictionary(data_dict, coloumn_0, coloumn_1, processing)
    fp.close()
    return data_dict


def calculate_average_word_count(data_dict):
    '''
    Arguemnts: data_dict(dictionary)
    makes an empty dicionary
    runs a for loop checking everything through dictionary
        makes a variable the length of the values in the dictionary
        make a variable valued at 0
        runs another for loop checking the nested dictionary
            adds the length of the value to the variable that was initially zero
        checks if the length of the values in the very initial dictionary is more than zero
            if it is then makes the singer as key in the initial empty dictionary and the total word/ total song as value

    returns the dictionary
    '''
    average_word_counts = {}

    for singer, songs in data_dict.items():
        total_songs = len(songs)
        total_words = 0

        for songs, lyrics in songs.items():
            total_words += len(lyrics)

        if total_songs > 0:
            average_word_counts[singer] = total_words / total_songs

    return average_word_counts


def find_singers_vocab(data_dict):
    '''
    Arguments: data_dict(dictionary)
    runs a for loop through the data_dict
        makes an empty list
        runs a for loop for the value in the data_dict
            runs a for loop for the values
                adds those words in the empty list

        makes the list a set
        adds the singer and set as key and value in the initial dictionary
    returns the dictionary
    '''
    dict_1 = {}

    for singers, songs in data_dict.items():
        list_1 = []

        for songs, lyrics in songs.items():
            for words in lyrics:
                list_1.append(words)

        myset = set(list_1)
        dict_1[singers] = myset

    return dict_1


def display_singers(combined_list):
    '''
    Arguemnts: combined list
    makes a sorted list
    prints the header
    then runs a for loop printing the top 10 singer in the sorted list
        prints the data
    '''
    sorted_list = sorted(combined_list, key=itemgetter(1, 3), reverse=True)

    # Display the Data
    print("\n{:^80s}".format("Singers by Average Word Count (TOP - 10)"))
    print("{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer", "Average Word Count", "Vocabulary Size", "Number of Songs"))
    print('-' * 80)

    for item in sorted_list[:10]:
        print("{:<20s}{:>20.2f}{:>20d}{:>20d}".format(item[0], item[1], item[3], item[2]))


def search_songs(data_dict, words):
    '''
    Arguments: data_dict(dictionary), words(string)
    makes a list for word in the words argument)
    runs a for loop from the dictionary
        runs a for loop through the values(nested dictionary)
            makes a set for the values inside
            checks if the set of words in the arguments is in the set created
                if it is then it will append the singer name and song name to the initial empty string
    returns a sorted list
    '''
    matching_songs = []
    # make sure that the words are lowercase
    words = [word.lower() for word in words]

    for singer, songs in data_dict.items():
        for song_name, song_lyrics in songs.items():
            song_words = set(song_lyrics)

            if set(words).issubset(song_words):
                matching_songs.append((singer, song_name))

    return sorted(matching_songs, key=itemgetter(0, 1))


def main():
    '''
    takes no argument
    opens stopwords
    opens song data
    calculates the average word count
    finds singer vocab
    makes an empty list
    runs a for loop in the dictionary
        makes a variable equal to length of values
        average words count makes a variable that is the average of key
        makes a variable that is the length of the key
        then appends them to the list in the order singer, avg_word_count, num_songs, vocab_size
    make a tuple for every singer : (singer_name, avg_word_count, num_songs, vocab_size)
    using the display function it displays
    prints search lyrics by words
    runs a while loop
        asks for input
        checks if the word is not valid
            prompts error message
        if there is nothing entered
            breaks the loop
        make a variable using the function search_song it finds the songs
        prints the length of the variable
        if the length of varible is more than 0
            prints the header
            runs a for loop
                prints the top 5 singer and the song

    '''
    # Open the stop words file and read the data
    stopwords_input = open_file('stopwords')
    stopwords = read_stopwords(stopwords_input)

    # Open the song data file and read the data
    song_data_file_input = open_file('song data')
    song_data_file = read_data(song_data_file_input, stopwords)

    # Calculate the average word count for each singer
    average = calculate_average_word_count(song_data_file)
    vocabulary = find_singers_vocab(song_data_file)
    results = []

    # Create a list of tuples for each singer : (singer_name, avg_word_count, num_songs, vocab_size)
    for singer, songs in song_data_file.items():
        num_songs = len(songs)
        avg_word_count = average[singer]
        vocab_size = len(vocabulary[singer])
        results.append((singer, avg_word_count, num_songs, vocab_size))

    # Combined list -- tuple for every singer : (singer_name, avg_word_count, num_songs, vocab_size)
    combined_list = sorted(results, key=itemgetter(2), reverse=True)
    display_singers(combined_list)

    # Search for songs
    print("\nSearch Lyrics by Words")
    while True:
        words = input("\nInput a set of words (space separated), press enter to exit: ").split()

        if not all([validate_word(word, stopwords) for word in words]):
            print("\nError in words!")
            print("1-) Words should not have any digit or punctuation")
            print("2-) Word list should not include any stop-word")
            continue

        if words == []:
            break

        matching_songs = search_songs(song_data_file, words)
        print("\nThere are {} songs containing the given words!".format(len(matching_songs)))

        if (len(matching_songs) > 0):
            print("{:<20s} {:<s}".format("Singer", "Song"))
            for singer, song_name in matching_songs[:5]:
                print("{:<20s} {:<s}".format(singer, song_name))


if __name__ == '__main__':
    main()
