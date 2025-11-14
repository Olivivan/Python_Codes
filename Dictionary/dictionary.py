import json
from difflib import get_close_matches

def get_definition(w):
    
    if w in data:
        return data[w]
    elif w.title() in data:
        return data[w.title()]
    elif w.upper() in data: #in case user enters words like USA or NATO
        return data[w.upper()]
    elif len(get_close_matches(w, data.keys())) > 0:
        yn = input("Did you mean %s instead? Enter Y if yes, or N if no: " % get_close_matches(w, data.keys())[0])
        if yn == "Y":
            return data[get_close_matches(w, data.keys())[0]]
        elif yn == "N":
            return "The word doesn't exist. Please double check it."
        else:
            return "We didn't understand your entry."
    else:
        return "The word doesn't exist. Please double check it."


data = json.load(open("D:/Python_Codes/Dictionary/data.json"))    
answer = "Y"

while answer == "Y":
    word = input("Enter word: ")
    word = word.lower()
    output = get_definition(word)

    if type(output) == list:
        for item in output:
            print(item)
    else:
        print(output)
    
    answer = input("Do you want to search another word? Enter Y for yes or N for no: ")   