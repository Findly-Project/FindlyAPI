from soupsieve.util import lower

set_exclusion_words = set(map(lower, ['Urggb', 'Unrjngrrng', 'Povrb']))
print(set_exclusion_words)