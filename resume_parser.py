"""
Resume Analyser
This will parse the file using tika service.
We do cleaning of the data to some extent.
Provides Author, Mobile Number, Email,
Top & Least 10 repeated words, Skills.
"""

import re
import sys
from collections import Counter

from tika import parser

# Parse the input file
parsed_doc = parser.from_file(sys.argv[1])
data = parsed_doc['content']

# Splitting into words for further purposes
words = data.split()

# Read stopwords from the file
stopwords = []
with open('stopwords.txt') as f:
    for line in f:
        stopwords.append(line.strip().lower())

# Read skills from the file
skills = []
with open('skill_master.txt') as f:
    for line in f:
        skills.append(line.strip().lower())

# Remove the stopwords/special chars from the content to improve some quality
filtered_words = []
special_chars = '''!()-[]{};:'"\,<>./?@#$%–^&*•_~·'''
skills_founded = []
for word in reversed(words):

    word = word.lower().strip()

    if word in stopwords:
        continue

    if word in special_chars: # Getting the special chars as most common
        continue

    if word in skills:
        skills_founded.append(word)

    filtered_words.append(word)

# Making the filtered words as a text to do a regex match for some fields
filtered_data = " ".join(filtered_words)

email = re.search(
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', # Partially googled this expression
    filtered_data).group()

mobile_number = re.search(r"[0-9]{10}", filtered_data).group()

# To find out the top 10 and least 10 repeated words
counter = Counter(filtered_words)
top_10_repeated_words = counter.most_common()

print("Author: " + parsed_doc['metadata'].get('Author', ''))
print("\nMobile Number: " + mobile_number)
print("\nEmail: " + email)
print("\nTop 10 repeated words: ")
for idx, word in enumerate(top_10_repeated_words):
    if idx == 10:
        break
    print("- " + word[0])

print('\nLeast 10 repeated words: ')
for idx, word in enumerate(reversed(top_10_repeated_words)):
    if idx == 10:
        break
    print('- ' + word[0])

print('\nSkills found in the resume: ')
for word in list(set(skills_founded)):
    print(word)
