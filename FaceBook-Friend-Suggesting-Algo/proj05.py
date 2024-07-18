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
#

'''Source header goes here'''



def open_file():
    '''
    Takes no Args,
    Asks for input from the user for a file name,
    makes a checking for the while loop to run
    goes into a while loop whenever the condition for it is True
        in the while loop goes through a try and exception
            in try it changes the condition so that the loop does not run again and opens the file in read view
            if the error comes "FileNotFoundError" then it prompts the message "Error in filename.", keep the condition for while loop at True and then asks for a file name input
    '''

    #loops the function to continuously for input of a file and if the file does not exist it shows and error message
    while True:
        try:
            file_name = input("Enter a file name: ")
            fp= open(file_name, 'r')
            return fp

        except FileNotFoundError:
            print("Error in filename.")



def read_file(fp):
    '''
    Takes one Argument
    creates an empty list and then reads the first line in the file and removes spaces and converts it to an integer
    runs a loop till the number of entries in the data file and appends empty list in the list created at the start
    runs another loop reading in for the argument entered and appends the user_id that are friends with 0,1,2 and so on to the initial empty list created
    at the end it returns that list
    fp : the number of users in the data file(int)
    Returns: the network of people who are friends with different users
    '''


    network = []
    n = int(fp.readline().strip())

    for i in range(n):
        network.append([])

    for line in fp:
        u, v = map(int, line.strip().split())
        network[u].append(v)
        network[v].append(u)

    return network


def num_in_common_between_lists(list1, list2):
    '''
    Takes two Arguments
    creates a list of the items that are common in the two Arguments inputed
    and returns the length of the list
    list1: the first arugment list
    '''

    common_item = [item for item in list1 if item in list2]
    return len(common_item)

def calc_similarity_scores(network):
    """
    takes one Argument (list)
    gets the length of the Argument, then makes a new list having same number of lists as the lenght of the argument
    then runs a loop in the range of the lenght of the argument, then runs another loop in the range of the lenght of the argument
    using the num_in_common_between_lists function it finds the number that is common between the two users and appends it in the correct list inside the similartiy_mat
    and returns the similarity_mat
    takes: network(list)
    returns: similarity_mat(list)
    """
    n = len(network)
    similarity_mat = [[0] * n for i in range(n)]

    for user1 in range(n):
        for user2 in range(n):
            num_common_friends = num_in_common_between_lists(network[user1], network[user2])
            similarity_mat[user1][user2] = num_common_friends

    return similarity_mat


def recommend(user_id, network, similarity_mat):
    '''
    Takes three arguments, user_id (int), network(list), similarity_mat(list)
    It then takes value from similarity_mat from the using the user_id as index
    it then checks the index of each character inside the similarity_score list along with the character itself, then if the index is same as the user_id it would continue or if the index is in the user_id index in the network list
    then if the value if more than max_similarity that we defined initially it will change the max_similarity variable to the character and the most_similar_user variable to the index of the character
    then returns the most_similar_user variable
    '''

    similarity_score = similarity_mat [user_id]
    most_similar_user = -1
    max_similartiy = -1

    for idx, score in enumerate(similarity_score):
        if idx == user_id or idx in network[user_id]:
            continue

        if score > max_similartiy:
            max_similartiy = score
            most_similar_user = idx

    return most_similar_user



def main():
    '''
    prints the intro prompt
    then defines a variable, "network" where using the open_file function and read_file function it becomes a list
    then defines another variable that is the length of the network variable minus one
    gives a variable, "cont_input" as "yes"
    runs a while loop for when cont_input is "yes"
    runs another while loop and inside it it asks the user for a input that is an integer, if the input is not in the range from 0 to the number of users in the data file then it prints and error message and reasks for an input
    if the user inputs anything apart from an integer then it shows an error message and asks again for an input
    once it gets the correct input, then using the calc_similarity_scores function assignes the value to another variable
    then using the recommend function it gets the integer the program should output
    it then prompt the user with a message for suggest friend for that user
    and asks the user of they want to run the loop again
    '''
    print("Facebook friend recommendation.\n")
    network = read_file(open_file())
    network_size = len(network) - 1
    cont_input = "yes"

    while cont_input == "yes":

        while True:
            try:
                int_input = int(input(f"\nEnter an integer in the range 0 to {network_size}: "))
                if 0 <= int_input <= network_size:
                    break
                else:
                    print(f"\nError: input must be an int between 0 and {network_size}")

            except ValueError:
                print(f"\nError: input must be an int between 0 and {network_size}")

        similarity_matrix = calc_similarity_scores(network)
        rec_friend = recommend(int_input, network, similarity_matrix)
        print(f"\nThe suggested friend for {int_input} is {rec_friend}")

        cont_input = input("\nDo you want to continue (yes/no)? ").lower()


if __name__ == "__main__":
    main()

