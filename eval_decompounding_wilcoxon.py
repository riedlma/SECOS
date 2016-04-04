import os
import sys
import re
import scipy.stats
from operator import add
import operator

if len(sys.argv)<7:
    print "this script performs an evaluation of two methods for compound splitting and also computes a wilcoxon test based on the F measure for each compound"
    print "python %s compound_1_file compound_1_column_predicted compound_1_column_gold compound_2_file compound_2_column_predicted compound_2_column_gold "%(sys.argv[0]) 
    sys.exit(0)
f1 = sys.argv[1]
f1_col_split = int(sys.argv[2])
f1_col_gold = int(sys.argv[3])
f2 = sys.argv[4]
f2_col_split = int(sys.argv[5])
f2_col_gold = int(sys.argv[6])
outp = False
if len(sys.argv)>7:
    outp=True

def getIdx(w):
    ws = w.split("-")
    i=0
    idx = []
    for s in ws:
        i+=len(s)
        idx.append(i)
    return idx


def evaluate(w1,w2):
    cc=0 #correct splits
    wfc = 0 # compound wrong split
    wnc = 0 # compound not split
    w1i = set(getIdx(w1))
    w2i = set(getIdx(w2))
    cc = len(w1i & w2i)
    wnc = len(w1i-w2i)
    wfc = len(w2i-w1i)
    
    return [cc,wfc,wnc]
def printEval(scores,a,c):
    k = scores
    print scores
    p = 1.0*k[0]/(1.0*k[0]+k[1])
    r = 1.0*k[0]/(1.0*k[0]+k[1]+k[2])
    f = 2*p*r/(p+r)
    sys.stderr.write("%f\t%f\t%f\n"%(p,r,f))
    sys.stderr.write("%f\t%f\t%f\n"%(a,c,1.0*c/a))

    sys.stderr.write("%10.4f & %10.4f&%10.4f\n"%(p,r,f))
    sys.stderr.write("%f\t%f\t%f\n"%(a,c,1.0*c/a))

a1=0
a2=0
c1=0
c2=0
scores1=[0,0,0]
scores2=[0,0,0]
f1_lines = open(f1).readlines()
f2_lines = open(f2).readlines()
if len(f1_lines)!=len(f2_lines):
    print "files have not same length"
    sys.exit(0)
def computeEvalSc(k):
    p = 1.0*k[0]/(1.0*k[0]+k[1])
    r = 1.0*k[0]/(1.0*k[0]+k[1]+k[2])
    if k[0]==0:
        f=0.0
    else:
        f = 2*p*r/(p+r)
    return [p,r,f]
x1=[]
x2=[]
xd = []
mcn = [[0,0],[0,0]]
for i in range(0,len(f1_lines)):
    #if not re.match(col_prefix,l.strip()):
    #    continue
    
    ls1 = f1_lines[i].strip().split("\t")
    ls2 = f2_lines[i].strip().split("\t")
    
    gold1 = ls1[f1_col_gold].lower()
    gold2 = ls2[f2_col_gold].lower()
    if gold1 != gold2:
        print "inequal: %s\t%s"%(gold1,gold2)
        print f1_lines[i].strip()
        print f2_lines[i].strip()
    cand1 = ls1[f1_col_split].lower()
    cand2 = ls2[f2_col_split].lower()
    sc1 = evaluate(gold1,cand1)
    sc2 = evaluate(gold2,cand2)
    e1 = computeEvalSc(sc1)
    e2 = computeEvalSc(sc2)
    if outp: print "%f\t%f\t%s\t%s\t%s"%(e1[2],e2[2],cand1,cand2,gold1)
    x1.append(e1[2])
    x2.append(e2[2])
    xd.append(e2[2]-e1[2])
    scores1=map(add, scores1, sc1)
    scores2=map(add, scores2, sc2)
    flag1 = "0"
    flag2 = "0"
    i1 = 0
    i2 = 0 
    if gold2 ==cand2:
        flag2 = "1"
        c2+=1
        i1=1
    if gold1 ==cand1:
        flag1 = "1"
        c1+=1
        i2=1
    mcn[i1][i2]+=1
    if outp :
        print flag1+"\t"+f1_lines[i].strip()
        print flag2+"\t"+f2_lines[i].strip()
    a1+=1
    a2+=1
print f1
printEval(scores1,a1,c1)
print f2
printEval(scores2,a2,c2)
#print mcn
#print mcnemar.mcnemar(mcn[0][1],mcn[1][0],mcn[0][0],mcn[1][1],0.05,verbose=True)
#print "test"
#print mcnemar.mcnemar2(mcn[0][1],mcn[1][0],mcn[0][0],mcn[1][1])
print "Wilcox"
print scipy.stats.wilcoxon(x1, y=x2, zero_method='wilcox')
print scipy.stats.wilcoxon(x2, y=x1, zero_method='wilcox')
print "Wilcox2"
print scipy.stats.wilcoxon(xd, zero_method='wilcox')
#k = scores
#print scores
#p = 1.0*k[0]/(1.0*k[0]+k[1])
#r = 1.0*k[0]/(1.0*k[0]+k[1]+k[2])
#f = 2*p*r/(p+r)
#sys.stderr.write("%f\t%f\t%f\n"%(p,r,f))
#sys.stderr.write("%f\t%f\t%f\n"%(a,c,1.0*c/a))
#
#sys.stderr.write("%10.4f & %10.4f&%10.4f\n"%(p,r,f))
#sys.stderr.write("%f\t%f\t%f\n"%(a,c,1.0*c/a))
