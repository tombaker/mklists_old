rules = [['0', 'i', 'a.txt', 'b.txt', '0']]
lines = ['two ticks\n', 'an ant\n', 'the mite\n']
output = {'a.txt': ['an ant\n'], 'b.txt': ['two ticks\n', 'the mite\n']}

rules = [['2', 'i', 'a.txt', 'b.txt', '1']]
lines = ['two ticks\n', 'an ant\n', 'the mite\n']
output = {'a.txt': ['an ant\n'], 'b.txt': ['the mite\n', 'two ticks\n']}
