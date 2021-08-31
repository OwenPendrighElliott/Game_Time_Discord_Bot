import sys
from itertools import combinations

class letters_game():
    def __init__(self, letters, words=None):
        letters = letters.lower()
        # by default use the unix words file
        if words == None:
            wl = open('/usr/share/dict/words', 'r')
        else:
            wl = open(words, 'r')

        wordlist = wl.readlines()
        wl.close()
        
        self.letters = [*letters]

        self.words = {}
        for wrd in wordlist:
            self.words[tuple(sorted(list(wrd)[:-1]))] = wrd[:-1]

        print(f"There are {len(self.words)} words in the dictionary")

    def solve(self):
        for i in range(9, 1, -1):
            wrds = combinations(self.letters, i)
            for wrd in wrds:
                if tuple(sorted(list(wrd))) in self.words:
                    print(f"A word of length {len(wrd)} was found")
                    return ''.join(c for c in self.words[tuple(sorted(list(wrd)))])

        raise Exception("No words could be made!")

# run file directly if wanted
def main():
    letters = sys.argv[1].lower()
    if len(sys.argv)>2:
    	words = sys.argv[2]
    else:
    	words = None
    game = letters_game(letters, words)
    sol = game.solve()
    
    print(sol)
        
if __name__ == '__main__':
    main()















