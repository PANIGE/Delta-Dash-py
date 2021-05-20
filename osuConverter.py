#Converter .osu taiko maps to DeltaDash maps, dirty writing but that works so i don't care

url = input("Please drop .osu here >>> ")
url = url.replace("\\", "/")
url = url.replace("\"", "")
AR = input("Please enter your note speed >>>")
HP = input("Please enter your health drain >>>")
OD = input("Please enter your Accuracy needed >>>")
SR = input("Please enter your beatmap difficulty selecting other maps around >>> ")

with open(url) as f:
    data = f.read()

data = data.split("\n")
result = f"{SR}|{AR}|{HP}|{OD}\n"

i = 1
for x in data:
    if x.startswith("[HitObjects]"):
        index = i
        break
    i += 1

hitObjects = data[i:]
for hobject in hitObjects:
    try:
        hobject = hobject.split(",")
        pos = 0 if int(hobject[4]) == 8 else 1
        result += "{}|{}\n".format(hobject[2], pos)
    except:
        pass
result = result[:len(result)-1] #Remove end backrow

with open("result.dd", "w") as f:
    f.write(result)

input("Written in \"result.dd\" please place it and rename it into your map folder")