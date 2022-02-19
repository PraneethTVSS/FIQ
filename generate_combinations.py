import itertools

input_data = input("Enter your text: ")

len_of_input = len(input_data)

for combination_length in range(len_of_input):
    # Generate the different length of combinations of strings
    combinations = itertools.combinations(input_data, combination_length)
    for combination in combinations:
        print("".join(combination))
