"""
   Searches deep inside a directory structure, looking for duplicate file.
   Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = "Patrick Ellis"
__email__ = "ellisp3@my.erau.edu"
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare


def search(file_list):
   """Looking for duplicate files in the provided list of files
   :returns a list of lists, where each list contains files with the same content

   Basic search strategy goes like this:
   - until the provided list is empty.
   - remove the 1st item from the provided file_list
   - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
   - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
   As a result we have a list, each item of that list is a list,
   each of those lists contains files that have the same content
   """
   lol = []
   flSize = list(map(getsize, file_list))
   file_list = list(filter(lambda x: 1 < flSize.count(getsize(x)), file_list))
   while 0 < len(file_list):
       tempLst = [file_list.pop(0)]
       for i in range(len(file_list) - 1, -1, -1):
           if compare(tempLst[0], file_list[i]):
               tempLst.append(file_list.pop(i))
       if len(tempLst) > 1:
           lol.append(tempLst)
   return lol

def faster_search(file_list):
   """Looking for duplicate files in the provided list of files
   :returns a list of lists, where each list contains files with the same content

   Here's an idea: executing the compare() function seems to take a lot of time.
   Therefore, let's optimize and try to call it a little less often.
   """
   #Once I found a faster method I would replace the other method with it so I could try to optimise it further
   #This method is the same as the one above because I couldn't find a way to optimise it further
   #This method is faster most of the time by about .05 sec but they're essentially the same
   lol = []
   flSize = list(map(getsize, file_list))
   file_list = list(filter(lambda x: 1 < flSize.count(getsize(x)), file_list))
   while 0 < len(file_list):
       tempLst = [file_list.pop(0)]
       [tempLst.append(file_list.pop(i)) for i in range(len(file_list) - 1, -1, -1) if compare(tempLst[0], file_list[i])]
       if len(tempLst) > 1:
           lol.append(tempLst)
   return lol


def report(lol):
   """ Prints a report
   :param lol: list of lists (each containing files with equal content)
   :return: None
   Prints a report:
   - longest list, i.e. the files with the most duplicates
   - list where the items require the largest amount or disk-space
   """
   print("== == Duplicate File Finder Report == ==")
   if len(lol) > 0:
       print(f"The file with the most duplicates is:\n{max(lol,key=lambda x : len(x))[0]}\nHere are its {len(max(lol,key=lambda x : len(x)))-1} copies:")
       print(*max(lol,key=lambda x : len(x))[1 ::], sep = "\n")
       mstSp = max(lol,key=lambda x : sum([getsize(i) for i in x]))
       mxSp = sum([getsize(mstSp[i]) for i in range(len(mstSp))])
       print(f"\nThe most disk space ({mxSp}) could be recovered, by deleting copies of this file: \n{max(lol,key=lambda x : sum([getsize(i) for i in x]))[0]}")
       print(f"Here are its {len(mstSp) - 1} copies")
       print(*max(lol,key=lambda x : sum([getsize(i) for i in x]))[1 ::], sep = "\n")


   else:
        print("No duplicates found")


if __name__ == '__main__':
    path = join(".", "images")
    #the path to the image folder on my computer
    path = "C:\\Users\\Patri\\OneDrive\\Desktop\\Project1\\Project1\\images"
   # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now w/ a faster search implementation:")

   # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Runtime: {time() - t0:.2f} seconds")
