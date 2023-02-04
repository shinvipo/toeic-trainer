import json

with open("./Data/question.json") as f:
    excecise = json.load(f)["questions"]
    
print(excecise[0])

for i,x in excecise[0].items():
    print(i,x)