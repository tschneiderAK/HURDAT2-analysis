import re

source = r"./hurdat_sample.txt"
name = "myTestSource"

with open(source) as s:
    sr = s.read()
    sr = '\n'.split(sr)
    print(sr)

