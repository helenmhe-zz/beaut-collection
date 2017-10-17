from bs4 import BeautifulSoup
import requests

class Trie:
    ##################################################
    ## basic methods
    ##################################################

    def __init__(self):
        self.frequency = 0
        self.children = {}

    # add word/frequency to the trie.  Increment frequency
    # if no value supplied.
    def insert(self, word, frequency=None):
        let = word[:1]
        if let not in self.children:
            self.children[let] = Trie()
        #Inserts each letter of the word, incrementing on the last letter
        if len(word) == 1:
            if frequency == None:
                self.children[let].frequency += 1
            else:
                self.children[let].frequency = frequency
        else:
            self.children[let].insert(word[1:], frequency)

    # return trie node for specified prefix, None if not in trie
    def find(self,prefix):
        if len(prefix) == 0:
            return self
        else:
            #Checks the Trie for membership of each letter in the prefix
            let = prefix[:1]
            if let in self.children:
                if len(prefix) == 1:
                    return self.children[let]
                else:
                    return self.children[let].find(prefix[1:])
            else:
                return None

    # is word in trie? return True or False
    def __contains__(self, word):
        node = self.find(word)
        return node != None and node.frequency != 0

    # return list of [word,freq] pairs for all words in
    # this trie and its children
    def __iter__(self):
        for i in self.iterhelper():
            yield i

    #Explores the Trie keeping track of checked nodes with prefix parameter
    #Yields within loops to make sure a list is returned and not a generator obj
    def iterhelper(self, prefix = ""):
        if self.frequency != 0:
            yield [prefix, self.frequency]
        for letter, trie in self.children.items():
            child = self.children[letter].iterhelper(prefix+letter)
            if child != None:
                for i in child:
                    yield i

    ##################################################
    ## additional methods
    ##################################################

    # return the list of N most-frequently occurring words that start with prefix.
    def autocomplete(self, prefix, N):
        """Reverse sort the list from find(prefix) using frequency (at index 1)

        Adds the prefix to each result and returns a slice of the first N
        """
        results = self.find(prefix)
        if results == None: return []
        wordlist = list(results)
        ans = []
        wordlist.sort(key=lambda x: x[1], reverse = True)
        for end in wordlist:
            ans.append(prefix+end[0])
        return ans[:N]

    # return the list of N most-frequent words that start with prefix or that
    # are valid words that differ from prefix by a small edit
    def autocorrect(self, prefix, N):
        complete = self.autocomplete(prefix, N)
        if len(complete) == N:
            return complete
        else:
            edits = self.make_edit(prefix)
            nodes = []
            for word in edits:
                if word in self:
                    # adds frequencies of word found if it matches exactly (no suffix)
                    nodes += [[word, trie[1]] for trie in list(self.find(word)) if len(trie[0])==0]
            # sort by frequency high to low
            nodes.sort(key=lambda x: x[1], reverse = True)
            # return the autocomplete results + unique autocorrect results
            return complete+[x[0] for x in nodes if x[0] not in complete][:N-len(complete)]

    # returns a set of edits for a word
    def make_edit(self, word):
        edits = set()

        for i in range(len(word)):
            # single character deletion
            edits.add(word[:i]+word[i+1:])
            # used ascii range
            for j in range(97,123):
                # single character replacement
                edits.add(word[:i]+chr(j)+word[i+1:])
                # single character insertion
                edits.add(word[:i]+chr(j)+word[i:])
                edits.add(word[:len(word)+1]+chr(j))
        # two letters transposed
        chars = list(word)
        for x in range(len(chars)):
            for y in range(x, len(chars)):
                chars[x], chars[y] = chars[y], chars[x]
                edits.add(''.join(chars))
                chars = list(word)

        return edits


    # return list of [word, freq] for all words in trie that match pattern
    # pattern is a string, interpreted as explained below
    #   * matches any sequence of zero or more characters
    #   ? matches any single character
    #   otherwise char in pattern char must equal char in word
    def filter(self,pattern):
        # populate a list of all words and filter them out, sort by alpha for debug
        allwords = []
        for i in self:
            allwords.append(i)
        filtered = self.filter_helper(pattern, filtered=allwords)
        self.allwords = []
        filtered.sort(key=lambda x: x[0])
        return filtered

    def filter_helper(self, pattern, index=0, ast= False, filtered=[]):
        # if every character has been filtered, filter out the suffixes unless ast (*)
        if pattern == "":
            new = []
            for word in filtered:
                if len(word[0]) == index or ast:
                    new.append(word)
            return new
        # current letter
        let = pattern[:1]
        if let == '*' :
            # if the only one is an asterisk return everything
            if len(pattern) == 1:
                return filtered
            # otherwise continue with the substring and set ast to True
            else:
                return self.filter_helper(pattern[1:], index, ast=True, filtered=filtered)
        # if ? then check if there's a character at index, increment index
        elif let == '?':
            new = []
            for word in filtered:
                if len(word[0][index:index+1]) != 0:
                    new.append(word)
            return self.filter_helper(pattern[1:], index+1, ast = False, filtered=new)
        else:
            # otherwise check if the letter at index matches
            new = []
            inds = []
            for word in filtered:
                if word[0][index:index+1] == let:
                    new.append(word)
                # if coming from a * then search the word for matches and add
                # the index of those matches to inds, a list of indices
                if ast and let in word[0]:
                    temp = word[0]
                    while let in temp:
                        s = [word[0].index(let, len(word[0])-len(temp)), word]
                        inds.append(s)
                        temp = temp[temp.index(let)+1:]
            # non asterisk branch
            all = self.filter_helper(pattern[1:], index+1, filtered=new)
            # if inds has elements then explore each branch at respective index
            for i in inds:
                branch = self.filter_helper(pattern[1:], index=i[0]+1, ast=False, filtered=[i[1]])
                if branch != []:
                    all += branch
            return all

# product = input("What type of product are you looking for? ")
# brand = input("Brand? ")
# rating = input("Min rating? ")
# color = input("Color adjectives? ")

# print('Input: ', product, brand, rating, color)

############################
# Getting Temptalia Brands #
############################

brands = 'https://www.temptalia.com/swatches/'
info = requests.get(brands)
soup = BeautifulSoup(info.content, "html.parser")
not_opts = ['Select a Brand...', 'All Brands']
brandlist = []
trie = Trie()
for link in soup.find_all('option'):
    current = link.text
    if str(current) not in not_opts:
        trie.insert(current.replace('-',' '),1)
        trie.insert(current.replace('-',' ').lower(),1)
        brandlist.append(current)
        brandlist.append(current.lower())

brand = input("Brand? ")
if brand and brand not in brandlist:
    options = trie.autocorrect(brand, 2)
    for op in options:
        change = input(f"Did you mean {op}? ")
        if change in ['true', '1', 't', 'y', 'yes', 'True', 'Yes', 'Y', 'T']:
            print(f"Searching for {op} instead!")
            brand = op
            break
    else:
        print(f"Looks like Temptalia doesn't have any reviews on hand for {brand} :(")

rating = input("Min rating? ")
if rating and rating not in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C-', 'D', 'F']:
    rating = input("In format of letter grade with +/- modifiers ")

colors = str.strip(input("Color adjectives? "))

print(colors)
