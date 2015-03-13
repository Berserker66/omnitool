import csv

itemlist = {}
i = 0
with open("sheet.csv") as source:
    data = csv.reader(source)
    for row in data:
        # print row
        if i > 0:
            #print row[1], row[5]
            itemlist[row[1]] = (
            int(row[5]), int(row[11]), int(row[12]), int(row[13]), int(row[14]), int(row[15]), row[19], row[23])
            #                   stack       damage         shoot          ammotype     isammotype        defense         acces     potion
        i += 1

weapons = []
text = "items = {"
i = len(text)
print(text)
s = " " * i
# print itemlist
for item in itemlist:
    trail = itemlist[item][-2] == "WAHR"
    trail2 = itemlist[item][-1] == "WAHR"
    itemlist[item] = itemlist[item][:-2] + (trail, trail2)
    #print itemlist[item][1]
    if itemlist[item][1] > 0:
        print(s + '"' + item + '":' + str(itemlist[item][0]) + ",")
        weapons.append(item)
print(s + "}")

