import sys
from itertools import permutations

class letters_game():
    def __init__(self, letters, words=None):
        # by default use the unix words file
        if words == None:
            wl = open('/usr/share/dict/words', 'r')
        else:
            wl = open(words, 'r')

        wordlist = wl.readlines()
        wl.close()
        
        self.letters = [*letters]
        self.words = {tuple(list(wrd.lower())[:-1]) for wrd in wordlist}
        print(f"There are {len(self.words)} words in the dictionary")

    def solve(self):
        # for every length get all permutations of the input string and check if they are words
        for i in range(9, 1, -1):
            wrds = permutations(self.letters, i)
            for wrd in wrds:
                if wrd in self.words:
                    print(f"A word of length {len(wrd)} was found")
                    return ''.join(c for c in wrd)

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















