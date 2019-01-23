# File: fake-news.py
# Author: YongBaek Cho
# Purpose: The program reads a csv file and print out key word that are frequently shown
# Date: 03/29/2018
import csv
import sys
import string
class Node():
    # An object of this Node class represents information about a word. It contains _word, _count, _next.
    def __init__(self,word): #initializes the object's attributes : _word is set to word, _count is set to 1;_nest is set to None.
        self._word = word
        self._count = 1
        self._next = None
    def word(self): # returns the value of _word
        return self._word # the word string
    def count(self): # returns the value of _count
        return self._count # a count of the number of occurrences of the word.
    def next(self): 
        return self._next # a reference to the next node in the linked list.
    def set_next(self,target): # sets the _next attribute to target.
        target._next = self._next
    def incr(self): # increments the value of _count
        self._count += 1
    def __str__(self): 
        return self.word()
class LinkedList: 
    # An object of this LinkedList class represents a linked list.

    def __init__(self): # initializes _head to None.
        self._head = None
    def is_empty(self): # returns a Boolean indicating whether or not the list contains any nodes.
        if self._head == None:
            return True
        else:
            return False
    def head(self): #returns a reference to the first node in the linked list, None if the list is empty.
            return self._head
    def update_count(self,word): #if word is present in the list, increments its count; otherwise, adds a node for it with count initialized to 1.
        if self.is_empty() is True:
            self._head = Node(word)
        else:
            curr_node = self._head
            while curr_node != None:
                if str(curr_node) == word :
                    curr_node.incr()
                    break
                if curr_node.next() == None:
                    curr_node._next = Node(word)
                    break
                curr_node = curr_node.next()
    def rm_from_hd(self): #removes the first node in the linked list and returns this node. It generates an error if this method is invoked on an empty list.
        x = self._head
        self._head = self._head.next()
        x._next = None
        return x
    def insert_after(self,node1,node2): # node1 and node2 are references to nodes. Inserts node2 into the list containing node1 so that the node that comes after node1 is node2.
        x = node1._next
        node1._next = node2
        node2._next = x
    def sort(self): #sorts the linked list in descending order by _count
        sorted = LinkedList()
        while self._head != None:
            curr_element = self.rm_from_hd()
            if sorted._head == None:
                sorted._head = curr_element
            else:
                x = sorted._head
                while x != None:
                    if curr_element.count() > x.count():
                        e = x
                        sorted._head = curr_element
                        sorted._head._next = e
                        break
                    if x.count() >= curr_element.count() and \
                            (x.next() == None or x._next.count()<curr_element.count()):
                        sorted.insert_after(x,curr_element)
                        break
                    x = x.next()
        self._head = sorted._head
    def get_nth_highest_count(self,n): # returns the count associated with the node in the linked list at position n.
        curr_node = self._head
        nth = 1
        count = 0
        while curr_node != None:
            if nth == n:
                count = curr_node.count()
                break
            if curr_node.count() != curr_node.next().count():
                nth += 1
            curr_node = curr_node.next()
        return count
    def print_upto_count(self,thiscount): # print out all the words that have count at least n.
        curr_node = self._head
        while curr_node.count()>= thiscount:
            word = curr_node.word()
            count = curr_node.count()
            print("{} : {:d}".format(word, count))
            curr_node = curr_node.next()


def main():
    try:
        # use try method to report Error
        filename = input('File: ')
        file = csv.reader(open(filename))
    except IOError:
        # if the file cannot open, print a Error message and quit
        print("ERROR: Could not open file " + filename)
        sys.exit(1)
    try: 
        # use try method with read in an integer value N using
        n = int(input('N: '))
    except IOError:
        # if can not read N, then print a Error message
        print("ERROR: Could not read N")
        sys.exit(1)
    mylist = []
    for line in file:
        # run through each line of title
        if '#' not in line[0]: # ignore the line with #
            title = line[4].lower() # lower the case eliminate difference
            for element in string.punctuation:
                # replace every punctuation with whitespace
                if element in title:
                    title = title.replace(element," ")
            for word in title.split():
                if len(word)>2:
                    # ignore words length shorter than 2
                    count_word(word,mylist)
    sorted_list = sort(mylist)
    i = 0
    while sorted_list[i].count() >= sorted_list[n].count():
        print("{} : {:d}".format(sorted_list[i], sorted_list[i].count()))
        i += 1
def count_word(word,mylist):
    # the function count the frequency of word in a list and return a list with Node Object
    found = False
    for element in mylist:
        # run though the list
        if element.word() == word:
            # if found the word, increase the frequency
            element.incr()
            found = True
    if found == False:
        # if not found the word in list
        new_word = Node(word) # create a Node object for that word
        mylist.append(new_word) # add to the list

def sort(M):
    # the function divide list into two until the list can not be divided
    if len(M) <= 1:
        return M
    else:
        split_1 = len(M) // 2 # find the middle point of the list
        M1 = M[:split_1]
        M2 = M[split_1:]
        sortedM1 = sort(M1)
        sortedM2 = sort(M2)
        return combined(sortedM1 , sortedM2)
def combined(first,second):
    # the function takes two list as parameter and returns a sorted list
    if not len(first) or not len(second):
        return first or second
    result = []
    i,j = 0,0
    while (len(result)<len(first)+len(second)):
        if first[i].count() > second[j].count(): # if first count is bigger than second count
            result.append(first[i]) # append the first one
            i += 1
        elif first[i].count() == second[j].count(): # if two has the same count
            if str(first[i]) < str(second[j]): # if first is lexicographically less than second
                result.append(first[i]) # append first
                i += 1
            else:
                result.append(second[j])
                j += 1
        else:
            result.append(second[j])
            j += 1
        if i == len(first) or j == len(second):
            result.extend(first[i:] or second[j:])
            break
    return result
main()