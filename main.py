# Name: Ben Peters
# Date: 12/3/2019
# Section: 004
# Purpose: To find book recommendations for the user based off their rating of various books compared with ratings by
#          other users
# Pre-Conditions: User inputs their name (stored as string), and their rating (-5, -3, 0, 1, 3, 5) of the books in the
#                 database (stored as list)
# Post-Conditions: Outputs user's name and ratings, most similar customer's name and ratings, and book recommendations


# get books function
def get_books():
    # Purpose: To create and return a 2D list of author's name and their book titles based off of file
    # Pre-Conditions: No parameters, reads from file
    # Post-Conditions: Returns list created
    # open file, assign to booklst
    booklst = open("books.txt")
    # create list based on lines in booklst
    books = booklst.readlines()
    # close file
    booklst.close()
    # strip and delimit on comma every book to make 2D list
    for i in range(len(books)):
        books[i] = books[i].strip()
        books[i] = books[i].split(",")
    # return list
    return books

# get customers function
def get_customers():
    # Purpose: To create and return a 2D list of customer names and their book ratings
    # Pre-Conditions: No parameters, reads from file
    # Post-Conditions: Returns list created
    # open file, assign to customerlst
    customerlst = open("customers.txt")
    # Create empty list to append to
    newcustlst = []
    # create list of lines of customerlst
    customers = customerlst.readlines()
    # close file
    customerlst.close()
    # strip and append to make 2d list
    for i in range(0,len(customers),2):
        newcustlst.append([customers[i].strip(), (customers[i+1].strip().split())])

    # convert digits to integers
    # for every customer in list
    for i in range(len(newcustlst)):
        # for every list of numbers in customer
        for num in newcustlst[0][1]:
            # for every rating in that list
            for j in range(len(newcustlst[i][1])):
                # change number from string to integer
                newcustlst[i][1][j] = int(newcustlst[i][1][j])

    # return list
    return newcustlst


# get user rankings function
def get_user_rankings(book_lst):
    # Purpose: To create and return a list of book ratings given by the user
    # Pre-Conditions: List of book information
    # Post-Conditions: Returns list created
    # create empty list to append to
    rankings = []

    # Print book name and get ranking from user, validating each input
    for book in book_lst:
        print(book[0], book[1])
        ranking = int(input("Ranking?: "))
        # validate inputs
        while ranking not in [-5,-3,0,1,3,5]:
            print("Invalid ranking!")
            ranking = int(input("Ranking?: "))

        # Append each ranking to a list
        rankings.append(ranking)
    # return list
    return rankings


# calculate similarity function
def calculate_similarity(cust1,cust2):
    # Purpose: To calculate and return the similarity of two customers based on algorithm
    #          (multiplying corresponding elements and summing them all)
    # Pre-Conditions: Two customers' list with names and list of rankings
    # Post-Conditions: Returns similarity of the two customers based on algorithm
    # using accumulator and for loop, calculate similarity of two customers given
    # return accumulator value
    # set accumulator to 0
    similarity = 0
    # calculate similarity using formula and accumulator
    for i in range(len(cust1[1])):
        similarity += cust1[1][i] * cust2[1][i]
    # return accumulator
    return similarity



# get similarity function
def get_similarities(cust_info,user_info):
    # Purpose: To calculate and return a 2D list of how similar each customer is to the user based off calculate
    #          similarity function
    # Pre-Conditions: List of all customer info and list of user's book rating
    # Post-Conditions: Return list created
    # for every customer, calculate similarity with user using calculate similarity function
    # store similarity and that customer's name to list
    # return list
    # create empty list to append to
    similarities = []
    # calculate similarity for every customer to user using function
    for cust in cust_info:
        similarity = calculate_similarity(cust, user_info)
        similarities.append([similarity, cust[0]])
    # return list
    return similarities

# main function
def main():
    # Purpose: Controls overall program, calls other functions with appropriate arguments.
    # Pre-Conditions: No parameters, all input is supplied from other functions and their returns
    # Post-Conditions: Outputs book recommendations (highest rated book that the customer most similar to the user has
    #                  read that the user hasn't read)
    # get list of books from function
    books = get_books()
    # get list of customers from function
    custs = get_customers()
    # print title
    print("Book Recommender")
    # get user's name
    name = input("What is your name? ")
    # call on get user ranking function, store value as ratings
    rankings = get_user_rankings(books)
    # create list of user's name and their rankings
    user = [name, rankings]
    # call on get similarity function, store list as simlst
    simlst = get_similarities(custs, user)
    # find customer most similar to user
    max_cust = max(simlst)
    # print customer most similar to user
    print("\nThis is your set of rankings\n", name, " ", rankings, sep="")
    print("\nThe customer with highest similarity", max_cust[1])
    # get rankings of most similar user
    for cust in custs:
        if cust[0] == max_cust[1]:
            sim_ratings = cust[1]
    # print most similar customer's ratings
    print("Their ratings", sim_ratings)

    # empty list to append to of books user hasn't read
    unread = []
    # empty list to append to
    sim_highest_unread = []
    # set value in case user has read every book
    sim_max = 0
    # find every book user hasn't read and which ones have highest rating from most similar customer with rating > 0
    for i in range(len(rankings)):
        # if user hasn't read book
        if rankings[i] == 0:
            # add book to list of unread books by user
            unread.append(books[i])
            # add score customer gave to book user hasn't read to list
            sim_highest_unread.append(sim_ratings[i])
            # find what the highest score the customer gave to all of the books the user hasn't read
            sim_max = max(sim_highest_unread)
    # empty list to append to
    sim_top = []
    # Find which books the customer gave the score which equals the highest score of books the user hasn't read, and the
    # book must have gotten a score of > 0
    for i in range(len(sim_ratings)):
        # if customer score equals max score given to all the books the user hasn't read and that score is > 0
        if sim_ratings[i] == sim_max and sim_ratings[i] > 0:
            # add book to list
            sim_top.append(books[i])
    # print out recommended books
    print("Recommendations:\n")
    # for every book user hasn't read, find which one is highest ranked by customer, accounting for multiple books having
    # same ranking
    num_recommended = 0
    for book in unread:
        if book in sim_top:
            print(book[0], ":", book[1])
            num_recommended += 1
    # if user has read every book in list
    if len(unread) == 0:
        print("No Recommendations! You've read all these!")
    else:
        print("\n",num_recommended, "recommendations")

main()
