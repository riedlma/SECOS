import os
import sys
import re

i=0

if len(sys.argv)<11:
    sys.stderr.write( "python "+sys.argv[0]+" dt_candidates word_count_file min_word_count(50) file_compound word_index prefix_length(3) suffix_length(3) word_length(5) dash_word(3) upper(upper) epsilon\n")
    sys.stderr.write("-----------------------------------------------------\n")
    sys.stderr.write("Parameter description:\n")
    sys.stderr.write("-----------------------------------------------------\n")
    sys.stderr.write("dt_candidates:\t\tfile with words and their split candidates, generated from a distributional thesaurus (DT)\n")
    sys.stderr.write("word_count_file:\tfile with word counts used for filtering\n")
    sys.stderr.write("min_word_count:\t\tminimal word count used for split candidates (recommended paramater: 50)\n")
    sys.stderr.write("file_compound:\t\tfile with words that should be decompounded (each compound needs to be in a single line)\n")
    sys.stderr.write("word_index:\t\tindex of the word in the tab separated file_compound\n")
    sys.stderr.write("prefix_length:\t\tlength of prefixes that are appended to the right-sided word (recommended parameter: 3)\n")
    sys.stderr.write("suffix_length:\t\tlength of suffixes that are appended to the left-sided word (recommended parameter: 3)\n")
    sys.stderr.write("word_length:\t\tminimal word length that is used from the split candidates (recommended parameter: 5)\n")
    sys.stderr.write("dash_word:\t\theuristic to split words with dash, which has no big impact (recommended: 3)\n")
    sys.stderr.write("upper:\t\t\tconsider uppercase letters (=upper) or not (=lower). Should be set for case-sensitive languages e.g. German\n")
    sys.stderr.write("epsilon:\t\tsmoothing factor (recommended parameter: 0.01\n")
    sys.exit(0)
file_knowledge = sys.argv[1]
file_wordcount = sys.argv[2]
min_word_count = int(sys.argv[3])
file_compound = sys.argv[4]
word_index_file_compound = int(sys.argv[5])


prefix_length = int(sys.argv[6])
suffix_length = int(sys.argv[7])
min_word_length = int(sys.argv[8])
epsilon = float(sys.argv[11])
sys.stderr.write(str(epsilon)+"\t:epsilon")
#1 -> remove, 2 -> split, 3 -> nothing
dash_words = int(sys.argv[9])
uppercaseFirstLetter=False
if sys.argv[10]=="upper":
    uppercaseFirstLetter=True


debug = True
debug = False
words = set()
total_word_count = 0
word_count = {}
for l in open(file_wordcount):
    ls = l.strip().split("\t")
    wc = int(ls[1])
    #if wc >=min_word_count:
    word_count[ls[0]]=wc
    total_word_count+=wc

def removeWord(w):
    if len(w.replace("-",""))==0:
        return True
    if min_word_count <=0:
        return False
    if w in word_count:
        if word_count[w]>=min_word_count:
            return False

    return True
def bylength(word1,word2):
    return len(word2)-len(word1)

def removeShortAndEqual(wc,ws):
    nws=set()
    for w in ws:
        if len(w)>=min_word_length and w.lower()!=wc.lower() and not w.isupper() and w.lower() in wc.lower():
            nws.add(w)
    return list(nws)
#count suffixes and prefixes
fillers = {}
def addUp(w):
    if w in fillers:
        fillers[w]+=1
    else:
        fillers[w]=1
def appendSuffix(w):
    nl = ""
    #first append on the left side
    for l in w.split("-"):
        if len(l)>suffix_length:
            nl+="-"
        else:
            addUp(l)
        nl+=l
    nl = nl.strip("-")
    return nl

def appendPrefix(w):
    #append to the right
    nw = w
    nl = ""
    for l in nw.split("-"):
        nl+=l
        if len(l)>prefix_length:
            nl+="-"
    if nl.endswith("-"):
        nl = nl[:-1]
    return nl
def getWordCounts(comp):
    sum = 1
    for c in comp.split("-"):
        if uppercaseFirstLetter:
            c = c[0].upper()+c[1:]
        if c in word_count:
            sum*=(word_count[c]+epsilon)/(total_word_count+epsilon*len(word_count))
        else:
            sum*=epsilon/(total_word_count+epsilon*len(word_count))
    return pow(1.0*sum,1.0/len(comp.split("-")))

def appendSuffixAndPrefix(w):
    sp = appendSuffix(appendPrefix(w))
    ps = appendPrefix(appendSuffix(w))
    spc = getWordCounts(sp)
    psc = getWordCounts(ps)
    #if w.replace("-","")=="Regionalliga":
    #    print "REGIONAL"
    #    print spc
    #    print psc
    #    print sp
    #    print ps
    if spc>psc:
        return sp
    return ps

def generateCompound(w,ws):
    #remove too short words
    #if debug: sys.out.write(ws
    nws = removeShortAndEqual(w,ws)
    #print nws
    if len(nws)==0:
        
        if debug: sys.stderr.write( "NONE: "+w+"\n")
        return None
    nws_sorted = sorted(nws,cmp=bylength,reverse=True)
    #get split points
    splits=set()
    for n in nws_sorted:
        if not n.lower() in w.lower():
            continue

        idx = w.lower().index(n.lower())
        splits.add(idx)
        splits.add(idx+len(n))
    splits_sorted = sorted(list(splits))
    #print nws_sorted
    #print splits_sorted
    wc = ""
    prev = 0
    for i in splits_sorted:
        if i==0:
            continue
        wc += w[prev:i]+"-"
        prev = i
    wc +=w[prev:]
    if wc.endswith("-"):
        wc = wc[:-1]
    return wc

def addCompound(comp,w,ws):
    if ws !=None:
        ws_merged = appendSuffixAndPrefix(ws)
        comp[w]=ws_merged
        if debug:sys.stderr.write( "Result: "+w+"\t"+ws+"\t"+ws_merged+"\n")
def processCompound(comp,w,wns):
    wns_split = wns.split(" ")
    if "-" in w and dash_words ==1:
        return
    if dash_words ==2:
        ws = w.split("-")
        for wi in ws:
            res = generateCompound(wi,wns_split)
            addCompound(comp,wi,res)
        return
    res = generateCompound(w,wns_split)
    addCompound(comp,w,res)
comp1 = {}
comp2 ={}
comp3 = {}
sys.stderr.write("read knowledge\n")
for l in open(file_knowledge):
    ls = l.rstrip("\n").split("\t")
    w = ls[0]
    if not removeWord(w):
        processCompound(comp1,w,ls[1])
        processCompound(comp2,w,ls[2])
        processCompound(comp3,w,ls[3])
sys.stderr.write("extract single words\n")
singlewords = set()
for c in comp1:
    if "-" in comp1[c]:
        singlewords|=set(comp1[c].split("-"))
sys.stderr.write("decompound")
#k = open("singlewords_martin","w")
#for s in singlewords:
#    k.write(s+"\n")
#close(k)
def containedIn(c,cands):
    for cj in cands:
        if c.lower() in cj.lower() and c.lower()!=cj.lower():
            return True
    return False
def unknownWordCompounding(w):
    cands = set()
    for s in singlewords:
        if s.lower() in w.lower()and not s.lower()==w.lower():
            cands.add(s)
    cands_new = set()
    for ci in cands:
        if not containedIn(ci,cands):
            cands_new.add(ci)
    res = generateCompound(w,cands_new)
    if debug: sys.stderr.write("unknown1: "+res+"\n")
    if res==None:
        res = w
    else:
        res = appendSuffixAndPrefix(res)
    if debug: sys.stderr.write("unknown2: "+res+"\n")
    return [res,cands_new]

def getFirstDash(compounds):
    i = 0
    for c in compounds:
        if "-" in c:
            return i
        i+=1
    return -1
def getMaxIdx(ls):
    idx = -1
    val = 0
    i=0
    for l in ls:
        if l>val:
            val = l
            idx = i
        i+=1 
    return [idx,val]

def getHighestProb(compounds):
    probs = []
    for c in compounds:
        p = getWordCounts(c)
        #if not "-" in c:
        #    p = p*-1
        probs.append(p)
    return getMaxIdx(probs)
    
               
for l in open(file_compound):
    ls = l.strip().split("\t")
    w = ls[word_index_file_compound]
    wc = -1
    if w in word_count:
        wc = word_count[w]
    c1 = comp1.get(w,w)
    c2 = comp2.get(w,w)
    c3 = comp3.get(w,w)
    [u,ufeats]=unknownWordCompounding(w)
    prefix = "W"
    cand = w
    feats = ""
    cands = [c1,c2,c3,u]
    cands_str = ["C1","C2","C3","U"]
    idx = getFirstDash(cands)
    if idx>=0:
        cand = cands[idx]
        prefix = cands_str[idx]
    [idx,prob] = getHighestProb(cands)
    pcand = w
    pprefix = "W"
    if idx>=0:
        #print cands
        #print idx
        pcand = cands[idx]
        pprefix = cands_str[idx]

    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\t%s" %(pprefix,pcand,prefix,cand,c1,c2,c3,u,l.strip(),wc,ufeats) 


    
