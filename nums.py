import sys
from collections import deque
import heapq
from itertools import combinations

class numbers_game():
    def __init__(self, goal, nums, trickshot=False):
        self.goal = goal
        self.nums = nums
        self.ops = [self.add, self.subtract, self.multiply, self.divide]
        self.trickshot = trickshot

    def add(self, a,b):
        return a+b
    
    def subtract(self, a,b):
        return a-b
    
    def multiply(self, a,b):
        return a*b
    
    def divide(self, a,b):
        '''
        Restricted divide to meet requirements of countdown
        '''
        if a == 0 or b == 0 or a%b != 0:
            raise ValueError("Invalid division for Countdown")
        return int(a/b)
    
    def h(self, nums):
        '''
        Heuristic for guessing how close we are
        If going for a trickshot then do the opposite
        '''
        if not self.trickshot:
            return abs(max(nums)-self.goal)
        else:
            return -abs(sum(nums)-self.goal)

    def solve(self):
        '''
        Best first search, follow the path with the lowest heuristic cost

        Not always optimal but is fast
        '''
        # initialise a heap for tracking progress
        Q = [(0, self.nums, [])]
        heapq.heapify(Q)
        nodes = 0
        while Q:
            cost, ns, path = heapq.heappop(Q)

            # check goal
            if self.goal in ns:
                print(f"Solution found after expanding {nodes} nodes")
                return path
            
            # if only one number is left then this path has failed
            if len(ns) <= 1:
                continue

            for a, b in combinations(ns, 2):
                # enforce largest first to allow for combinations instead of permutations
                if b > a:
                    a, b = b, a
                for op in self.ops:
                    nodes += 1
                    # try and calulate new value 
                    try:
                        new_n = op(a, b)
                    except ValueError:
                        continue
                    
                    # if value is negative then we dont need it
                    if new_n < 0:
                        continue

                    # create new list of numbers, new path and update cost
                    new_ns = list(ns)
                    new_ns.remove(a)
                    new_ns.remove(b)
                    new_ns.append(new_n)
                    new_path = list(path)
                    new_path.append((a, op.__name__, b, new_n))
                    path_cost = cost + self.h(new_ns)
                    heapq.heappush(Q, (path_cost, new_ns, new_path))
                    
        raise Exception("No Solution available!")

# run file directly if wanted
def main():
    ns_str = sys.argv[1]
    nums = [int(n) for n in ns_str.split('-')]
    goal = int(sys.argv[2])

    if len(sys.argv)>3:
    	trickshot = bool(sys.argv[3])
    else:
    	trickshot = False

    game = numbers_game(goal, nums, trickshot)
    sol = game.solve()
    
    for a, op, b, r in sol:
        print(f"{op.capitalize()} {a} and {b} to get {r}")
        
if __name__ == '__main__':
    main()

