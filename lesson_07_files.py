import csv
import os

# Flag to determine whether to delete the example files after execution
DELETE = False

# Writing to a text file
with open("example.txt", "w") as file:
    file.write("Hello, world!\n")
    file.write("This is a basic example of file handling in Python.\n")

# Reading from a text file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# Appending to a text file
with open("example.txt", "a") as file:
    file.write("Appending a new line to the file.\n")

# Writing to a CSV file
with open("example.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Name", "Age", "City"])
    csvwriter.writerow(["Jin", 30, "New York"])
    csvwriter.writerow(["Mirijam", 25, "Los Angeles"])
    csvwriter.writerow(["Zhang", 35, "Chicago"])

# Reading from a CSV file
with open("example.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        print(row)

if DELETE:
    # Deleting the example files
    os.remove("example.txt")
    os.remove("example.csv")
