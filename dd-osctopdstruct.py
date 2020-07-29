import os
import re
import functools
import sys

minmax = {"ppg:ir": {"min": 999999, "max": -999999}, "ppg:red": {"min": 999999, "max": -999999}, "ppg:grn": {"min": 999999, "max": -999999}, "eda": {"min": 999999, "max": -999999}, "temp": {"min": 999999, "max": -999999}, "therm": {"min": 999999, "max": -999999}, "humidity": {"min": 999999, "max": -999999}, "acc:x": {"min": 999999, "max": -999999}, "acc:y": {"min": 999999, "max": -999999}, "acc:z": {"min": 999999, "max": -999999}, "gyro:x": {"min": 999999, "max": -999999}, "gyro:y": {"min": 999999, "max": -999999}, "gyro:z":  {"min": 999999, "max": -999999}, "mag:x" : {"min": 999999, "max": -999999}, "mag:y": {"min": 999999, "max": -999999}, "mag:z": {"min": 999999, "max": -999999}}

prev = {"ppg:ir": 0, "ppg:red": 0, "ppg:grn": 0, "eda": 0, "temp": 0, "therm": 0, "humidity": 0, "acc:x": 0, "acc:y": 0, "acc:z": 0, "gyro:x": 0, "gyro:y": 0, "gyro:z":  0, "mag:x" : 0, "mag:y": 0, "mag:z": 0}
outlines = ["data", "template dancerdata", "float pos", "float numframes", "array oscdata emotibit", "", "template emotibit", "float x", "float ppg-ir", "float ppg-red", "float ppg-grn", "float eda", "float temp", "float therm", "float humidity", "float acc-x", "float acc-y", "float acc-z", "float gyro-x", "float gyro-y", "float gyro-z", "float mag-x", "float mag-y", "float mag-z", "", "template moving-cursor", "float x", ""]

filename = sys.argv[1]
curpath,curfile = os.path.split(filename)
basename,ext = os.path.splitext(curfile)
outfile = os.path.join(curpath, basename + ".pdstruct")

with open(filename) as f:
    curlines = f.read().splitlines()
    totlines = len(curlines)
    for line in curlines:
        databits = re.findall("/[^\s]*[^\s][^/]*", line.strip()) # splits into addresses and values
        cur = {}
        retStr = ""
        for databit in databits:
            dataparts = databit.strip().split(" ") # split into address and vals
            curAddr = dataparts[0] # cur address
            curVals = list(map(lambda x: float(x),dataparts[1:])) # current values
            curParam = curAddr.split("/")[-1].lower() # cur param of note lowercased for santiy's sake
            curVal = 0
            if len(curVals) > 1:
                curVal = functools.reduce(lambda x,y: x+y, curVals)/float(len(curVals))
            else:
                curVal = curVals[0]
            if curParam != "frame": 
                cur[curParam] = curVal
                if curVal > minmax[curParam]["max"]:
                    minmax[curParam]["max"] = curVal
                if curVal < minmax[curParam]["min"]:
                    minmax[curParam]["min"] = curVal
            else:
                cur[curParam] = curVal - 1 #is frame, make 0 index (instead of i index
        cur_frame = int(cur["frame"])
        if cur_frame % 1000 == 0:
            outlines += [""]
            if cur_frame == 0:
                outlines += ["moving-cursor 0"]
            outlines += ["dancerdata " + str(cur_frame) + " " + str(totlines)]
        retStr += str(cur_frame) + " "
        for idx,param in enumerate([*prev]):
            if param not in [*cur]:
               retStr += str(prev[param])
            else:
                retStr += str(cur[param])
                prev[param] = cur[param]
            if idx != len([*prev]) - 1:
                retStr += " "
        outlines += [retStr]

outlines += [""]

with open(outfile,"w") as f:
    f.writelines(x + ";\n" for x in outlines)

for k,v in minmax.items():
    for m,w in v.items():
        print(k,m,w)
