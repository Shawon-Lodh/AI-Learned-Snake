import json
# at first making a empty list based json file then append system is okk otherwise python doesn't find any json file
# with open("train_x_data.json", mode='w', encoding='utf-8') as f:
#     json.dump([], f)
# with open("train_y_data.json", mode='w', encoding='utf-8') as f1:
#     json.dump([], f1)


#see the json file
f = open("train_x_data.json")
d = json.load(f)

f1 = open("train_y_data.json")
d1 = json.load(f1)

for i,m in enumerate(d):
    print(d[i],d1[i])

