import xmltodict
#import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#with open('hupudata.xml') as inf, open('hupu.xml','w') as outf:
    #data = inf.read()
    #data = data.replace("\n", "")
    #outf.write(data)


with open('hupudata.xml') as file:
    doc = xmltodict.parse(file.read())
    #len(doc)

#sum([len(dia['s']) for dia in doc['hupudata']['dialog']])
#len(doc['hupudata']['dialog'])
#dialengths = [len(dia['s']) for dia in doc['hupudata']['dialog']]

dia_cnt = 0
s_cnt = 0
utt_cnt = 0

slens = []
uttlens = []
import math
for dia in doc['hupudata']['dialog']:
    dia_cnt += 1
    ss = dia['s']
    if type(ss) is not list:
        ss = [ss]
    s_cnt += len(ss)
    slens.append(len(ss))
    #print len(ss)
    for s in ss:
        utts = s['utt']
        if type(utts) is not list:
            utts = [utts]
        utt_cnt += len(utts)
        uttlens.append(len(utts))

plt.xlabel('number of <s> -- N')
plt.ylabel('frequency of dialogs with log(N) of <s>')
plt.title(r'Distribution of <s> -- in log scale')
plt.yscale('log', nonposy='clip')
plt.xticks(range(0,1000,100))
#plt.xscale('1')
plt.hist(slens)
plt.grid(True)
#plt.show()
plt.savefig('<s> distribution', bbox_inches='tight')

plt.xlabel('number of <utt> -- NX')
plt.yscale('log', nonposy='clip')
plt.ylabel('frequency of <s> with N of <utt>')
plt.title(r'Distribution of <utt>')
plt.hist(uttlens)
plt.grid(True)
plt.savefig('<utt> distribution', bbox_inches='tight')
#plt.show()

#print slens
print "Dias: " + str(dia_cnt)
print "Ss: " + str(s_cnt)
print "Utts: " + str(utt_cnt)
