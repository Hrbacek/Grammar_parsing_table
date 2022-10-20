import csv

input = {i:[] for i in range(5)}
with open("grammar.csv", "r") as file:
    data = csv.reader(file)
    i = 0
    for line in data:
        input[i] = line
        i += 1
input[3] = [production.split(":") for production in input[3]]

if __name__ == "__main__":
    print(input)
