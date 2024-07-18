import csv
import string
from operator import itemgetter



def open_file(message):
    check = True

    while True:

        try:
            file_name_input = input(('\nEnter a filename for the stopwords: '))
            file_object = open(file_name_input, "r")
            check = False
            return file_object

        except FileNotFoundError:
            print('\nError in words!')
            check = True


def read_stopwords(fp):
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

    return word.isalpha() and word not in stopwords


def process_lyrics(lyrics, stopwords):
    list_2= []

    lyrics_list = lyrics.split()
    for lyric_word in lyrics_list:
        lyric_word = lyric_word.strip().strip(string.punctuation)
        lyric_word = lyric_word.lower()

        if validate_word(lyric_word, stopwords) == True:
            list_2.append(lyric_word)
    set_2 = set(list_2)
    return set_2


def update_dictionary(data_dict, singer, song, words):

    song_dict = {}
    if (singer in data_dict):
        song_dict = data_dict[singer]

    (key, val) = song, words
    song_dict[key] = (val)

    (key, val) = singer, song_dict
    data_dict[key] = (val)


def read_data(fp, stopwords):
    reader = csv.reader(fp)
    next(reader)
    data_dict={}

    for row in reader:
        coloumn_0 = row[0]
        coloumn_1 = row[1]
        coloumn_2 = row[2].lower()

        processing = process_lyrics(coloumn_2, stopwords)

        update_dictionary(data_dict, coloumn_0, coloumn_1, processing)
    fp.close()
    return data_dict



def calculate_average_word_count(data_dict):
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
    ''' DocStrings goes here.'''

    "\n{:^80s}".format("Singers by Average Word Count (TOP - 10)")
    "{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer","Average Word Count", "Vocabulary Size", "Number of Songs")
    '-' * 80
    pass


def search_songs(data_dict, words):
    matching_songs = []

    for singer, songs in data_dict.items():
        for song_name, song_lyrics in songs.items():
            song_words = set(song_lyrics)

            if set(words).issubset(song_words):
                matching_songs.append((singer, song_name))

    return matching_songs

def main():

    stopwords_input = open_file()
    stopwords = read_stopwords(stopwords_input)

    song_data_file_input= input('\nEnter a filename for the song data: ')
    song_data_file = read_data(song_data_file_input, stopwords)

    average = calculate_average_word_count(song_data_file)

    vocabulary = find_singers_vocab(song_data_file)
    results = []

    for singer, songs in song_data_file.items():
        num_songs = len(songs)
        avg_word_count = average[singer]
        vocab_size = len(vocabulary[singer])
        results.append((singer, num_songs, avg_word_count, vocab_size))

    "\nSearch Lyrics by Words"


    "\nInput a set of words (space separated), press enter to exit: "
    '\nError in words!'
    "\nThere are {} songs containing the given words!"
    "{:<20s} {:<s}"
    pass
if __name__ == '__main__':
    main()
