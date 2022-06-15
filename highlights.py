# Created 6/7 by Mira Flynn for Pfizer GCS
# This code is intended to take 2 strings and output 2 html-formatted strings highlighting differences between them.
# The HTML for this is in a separate HTML file with a form with 2 string inputs, and 2 divs for the output results.
# The CSS is in a separate CSS file defining a highlight color for correct letters and incorecct letters.

# Note: I think it might be possible to inject some HTML via the form inputs. Depending on how widely this is used, someone might want to spend a bit considering that possibility. TBH not sure if it's possible or not, input sanitization isn't something I know much about.

import re
from collections.abc import Iterable

def findDiff(str1: str, str2: str, writeToFile: bool = False):
    '''
    findDiff()
    Take 2 strings and compare them. Highlight differences and return highlighted HTML string. This is the overall control function.
    If writeToFile is true, then write the output to view.md to visualize it
    Inputs: 
        str1: string
        str2: string
        writeToFile: bool = False
    Returns: length 2 tuple of strings
    '''

    lst1 = getWords(str1)
    lst2 = getWords(str2)

    # print(lst1)
    # print(lst2)

    formattedStr1, formattedStr2 = formatDiffs(lst1, lst2)

    if(writeToFile):
        writeHTML(formattedStr1 + "<br>" + formattedStr2)
    return (formattedStr1, formattedStr2)


def getChars(string: str):
    '''
    getChars(string)
    Takes str and splits into individual characters.
    Inputs:
        string: string
    Returns: list of characters
    '''
    return list(string)


def getWords(string: str):
    '''
    getWords(string)
    Takes str and splits into "words". Splits into each segment of alphanumeric characters and each segment of non-alphanumeric characters
    For example:
    abc def. ghi -> ["abc", " ", "def", ". ", "ghi"]
    Inputs:
        string: string
    Returns: list of strings
    '''
    pattern = r'([^A-Za-z0-9]+)'
    lst = re.split(pattern, string)
    if(lst[len(lst)-1] == ''):
        lst.pop()
    return lst


def formatDiffsNoLookahead(lst1: Iterable, lst2: Iterable):
    '''
    formatDiffsNoLookahead(lst1, lst2)
    Takes 2 lists and compares character by character. Constructs 2 HTML formatted strings showing which characters are different.
    Inputs:
        lst1: list
        lst2: list
    Returns: length 2 tuple of strings
    '''
    # I ended up re-using this function as a helper function within formatDiffs. If 2 words don't match, then they are compared character by character.
    # As this is being re-used within the larger generated HTML, this function no longer should include the preformatted tag

    # formattedStr1 = "<pre style='font-family:monospace'>"
    # formattedStr2 = "<pre style='font-family:monospace'>"
    formattedStr1 = ""
    formattedStr2 = ""

    for i in range(min(len(lst1), len(lst2))):
        if(lst1[i] == lst2[i]):
            formattedStr1 = addToString(formattedStr1, lst1[i], True)
            formattedStr2 = addToString(formattedStr2, lst2[i], True)
        else:
            formattedStr1 = formattedStr1 = addToString(formattedStr1, lst1[i], False)
            formattedStr2 = formattedStr2 = addToString(formattedStr2, lst2[i], False)
    if(len(lst1) > len(lst2)):
        for i in range(len(lst2), len(lst1)):
            formattedStr1 = addToString(formattedStr1, lst1[i], False)
    else:
        for i in range(len(lst1), len(lst2)):
            formattedStr2 = addToString(formattedStr2, lst2[i], False)
        
    # formattedStr1 += "</pre>"
    # formattedStr2 += "</pre>"

    return (formattedStr1, formattedStr2)


def formatDiffs(lst1: Iterable, lst2: Iterable):
    '''
    formatDiffs(lst1, lst2)
    Takes 2 lists and compares element by element, looking ahead for matches to account for added words. 
    Constructs 2 HTML formatted strings showing which elements are different.
    Inputs:
        lst1: list
        lst2: list
    Returns: length 2 tuple of strings
    '''

    # This function is really janky. Really, really, really janky.
    # It currently has manually defined cases for looking 1 and 2 elements ahead.
    # In the future, this should probably be rebuilt to check forward in a loop.

    formattedStr1 = "<pre style='font-family:monospace'>" # Add a pre so that multiple spaces are rendered as such.
    formattedStr2 = "<pre style='font-family:monospace'>"
    pos1 = 0
    pos2 = 0

    # Appending 2 empty elements to the ends of the lists so I can check 2 forward safely
    lst1.append('')
    lst1.append('')
    lst2.append('')
    lst2.append('')

    while(True):
        # The lists have 2 blank elements appended to the end. 
        # The blank elements can never be equal to any of the actual words because of the regex.
        # So if the positions are both less than the length - 2, then it's safe to check forward.
        # This case captures everything where neither list has reached the end.
        if(pos1 < len(lst1)-2 and pos2 < len(lst2)-2): 

            # If the two current words are equal, then write them both
            if(lst1[pos1] == lst2[pos2]):
                formattedStr1 = addToString(formattedStr1, lst1[pos1], True)
                formattedStr2 = addToString(formattedStr2, lst2[pos2], True)
                pos1 += 1
                pos2 += 1

            # If current word 1 matches next word 2, then add the current word 2 to realign
            elif(lst1[pos1] == lst2[pos2+1]):
                formattedStr2 = addToString(formattedStr2, lst2[pos2], False)
                pos1 += 1

            # If current word 2 matches next word 1, then add the current word 1 to realign
            elif(lst1[pos1+1] == lst2[pos2]):
                formattedStr1 = addToString(formattedStr1, lst1[pos1], False)
                pos2 += 1

            # If current word 1 matches 2 ahead word 2, then add the current and next word 2 to realign
            elif(lst1[pos1] == lst2[pos2+2]):
                formattedStr2 = addToString(formattedStr2, lst2[pos2], False)
                formattedStr2 = addToString(formattedStr2, lst2[pos2+1], False)
                pos2 += 2

            # If current word 2 matches 2 ahead word 1, then add the current and next word 1 to realign
            elif(lst1[pos1+2] == lst2[pos2]):
                formattedStr1 = addToString(formattedStr1, lst1[pos1], False)
                formattedStr1 = addToString(formattedStr1, lst1[pos1+1], False)
                pos1 += 2

            # If current, next, and 2 ahead all don't match, then these words don't match, move on
            # Compare non-match words character by character.
            else:
                # formattedStr1 = addToString(formattedStr1, lst1[pos1], False)
                # formattedStr2 = addToString(formattedStr2, lst2[pos2], False)
                word1 = getChars(lst1[pos1])
                word2 = getChars(lst2[pos2])
                formattedWord1, formattedWord2 = formatDiffsNoLookahead(word1, word2)
                formattedStr1 = formattedStr1 + formattedWord1
                formattedStr2 = formattedStr2 + formattedWord2
                pos1 += 1
                pos2 += 1

        # If both lists have reached their end, then break the while loop
        elif(pos1 == len(lst1)-2 and pos2 == len(lst2)-2): 
            break

        # If list 1 (and not list 2) has reached its end, add the next word in list 2
        elif(pos1 == len(lst1)-2):
            formattedStr2 = addToString(formattedStr2, lst2[pos2], False)
            pos2 += 1
        
        # If list 2 (and not list 1) has reached its end, add the next word in list 1.
        elif(pos2 == len(lst2)-2):
            formattedStr1 = addToString(formattedStr1, lst1[pos1], False)
            pos1 += 1
        else: 
            print("did we get here?")

            # All cases should be caught, so this break should never be reached. I just want to avoid an infinite loop.
            break
    
    formattedStr1 += "</pre>"
    formattedStr2 += "</pre>"

    return (formattedStr1, formattedStr2)

def addToString(base: str, element: str, correct: bool):
    '''
    addToString()
    Adds an element to the base string with HTML formatting
    Inputs:
        base: string
        element: string
        correct: bool
    Returns: string
    '''
    # This is essentially a shorthand to make the spans to make the formatDiffs code cleaner
    if(correct):
        return base + "<span>" + element + "</span>"
    
    return base + "<span style='background-color: lightcoral'>" + element + "</span>"

    

def writeHTML(content):
    '''
    writeHTML(content)
    Takes an html string. Writes to an md file so I can view the output for debugging
    Inputs:
        content: string
    Returns: none
    '''
    f = open("view.md", "w")
    f.write(content)
    f.close()



if __name__ == '__main__':
    # str1 = "string one 1 one."
    # str2 = "string 1 and one,one"
    str1 = "string one two three"
    str2 = "string One two three"
    print(findDiff(str1, str2, True))

    

