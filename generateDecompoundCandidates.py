import os
import sys
import re

dt = {}
i = 0
split_dash = False
acceptRegex=".*"
if len(sys.argv)>1:
    acceptRegex = sys.argv[1]
if len(sys.argv)>2:
    split_dash = True
accept = re.compile(acceptRegex)
prev = ""
for l in sys.stdin:
    ls = l.strip().split("\t")
    w1 = ls[0]
    w2 = ls[1]
    if not (accept.match(w1) and accept.match(w2)):
        sys.stderr.write("Not accepted: "+w1+"\t"+w2+"\n")
        continue

    
    if w1 in dt:
        dt[w1].append(w2)
    else:
        dt[w1]=[w2]
    if i%1000000==0:
        sys.stderr.write(str(i)+"\n")
    i+=1

def getOverlap(w,ls):
    wl = w.lower()
    ret = []
    for l in ls:
        if l.lower() in wl:
            ret.append(l)
        if split_dash and "-" in l:
            lm = l.split("-")
            for m in lm:
                if m in wl:
                    ret.append(l)
    return ret

def addset(d,s):
    for w in s:
        if w in d:
            d[w]+=1
        else:
            d[w]=1
    return d
j = 0
for w1 in dt:
    sims = dt[w1]
    word_overlap = getOverlap(w1,sims)
    sims_overlap = {}
    
    for w2 in sims:
        if w2 in dt:
            overlap = getOverlap(w1,dt[w2])
            sims_overlap = addset(sims_overlap,overlap)
    out1 = ""
    out2 = ""
    out3 = " ".join(word_overlap)
    for w2 in sims_overlap:
        out1+=" " +w2
        out2+=" "+w2+":"+str(sims_overlap[w2])
    out3 = out3+out1
    out1 = out1.strip()
    print w1+"\t"+" ".join(word_overlap)+"\t"+out1+"\t"+out3+"\t"+out2
    j+=1
    if j%1000000==0:
        sys.stderr.write(str(j)+"\t"+str(1.0*j/i)+"\n")
