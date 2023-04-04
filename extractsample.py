import re

source = r"./hurdat_sample.txt"
name = "myTestSource"

with open(source, 'r') as s:
    sr = s.readlines()

    print(sr)

