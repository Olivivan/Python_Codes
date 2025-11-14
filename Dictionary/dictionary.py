import json

data = json.load(open("D:/Python_Codes/Dictionary/data.json"))

def get_definition(word):
    """Retrieve the definition of a word from the loaded JSON data."""
    if word in data:
        return data[word]
    else:
        return print(f"The word '{word}' was not found in the dictionary. Try another word...")
    
    


word = input("Enter a word: ")
word = word.lower()

definition = get_definition(word)
print(f"Definition of {word}: {definition}")
