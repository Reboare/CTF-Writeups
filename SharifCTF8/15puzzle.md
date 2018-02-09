The challenge was to create a solver for the 15puzzle.  My solution is implemented below along with a link to the algorithm used.

```python
#https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
import re

puzzles = []

with open('puzzles.txt') as f_puzzles:
    r_puzzles = f_puzzles.read()
    for x in re.finditer("Puzzle for",r_puzzles):
        puzzle = r_puzzles[x.start():x.start()+132]
        puzzle = [x[1:-1].split('|') for x in puzzle.split('\n')[1:] if '+' not in x and x != '']
        puzzle = [item for sublist in puzzle for item in sublist]
        puzzle = [item.strip() for item in puzzle]
        puzzles.append(puzzle)
def is_soluble(i):
    #inversions
    puzzle = puzzles[i]
    inversions = []
    for i, x in enumerate(puzzle):
        if x == '':
            continue
        else:
            above = [int(d) for d in puzzle[i+1:] if d != '']
            inversions.append(sum(y > int(x) for y in above))
    inversion = sum(inversions)
    blank_position = puzzle.index('')
    if blank_position in [15,14,13,12,7,6,5,4]:
        if inversion%2 == 0:
            return 1
        else:
            return 0
    elif inversion %2 !=0 :
        return 1
    else:
        return 0
flag = ' '
for i in range(128):
     flag = ('1' if is_soluble(i) else '0') + flag
print('SharifCTF{%016x}' % int(flag, 2))
```
