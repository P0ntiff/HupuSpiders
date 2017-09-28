import json
from collections import defaultdict
import string
import codecs

outputName = "HupuSpiders_chi.xml"
fh = json.load(open('/Users/michliu/PycharmProjects/tst/hupu_rawdata.json', 'r'))
tpc = []
d = {}
for line in fh: # group by topic, return a dict type object [(tpcid,[{},{},...]), (tpcid,)]
    reply = line['reply_infos']
    tpcid = line['tid']
    for conv in reply:
        if conv['ori_floor'] > conv['pos_floor']:
            if tpcid not in tpc:
                tpc.append(tpcid)
            d.setdefault(tpcid, []).append(conv)
        else: continue


outputFile = codecs.open(outputName, "w", encoding='utf8')
outputFile.write(outputName + "\n")


uids = {}  #paired value, {url:#,}
for dia in tpc: #loop each topic
    floor = []  #floor numbers
    con = {}    # conversations
    outputFile.write("<dialog>\n") # start a dialog/topic

    for talk in d[dia]:#looping each conversation
        if len(talk['pos_message']) > 1 and len(talk['ori_message']) > 1:
            pid = talk['pos_id']
            oid = talk['ori_id']
            if pid not in uids:
                uids[pid]= len(uids) + 1
            if oid not in uids:
                uids[oid]= len(uids) + 1
        #

            if talk['pos_floor'] not in floor: # each utterance
                floor.append(talk['pos_floor'])
                floor.append(talk['ori_floor'])
                con.setdefault(talk['pos_floor'],[]).append('<utt uid="' + str(uids[pid]) + '">')
                con.setdefault(talk['pos_floor'], []).append(talk['pos_message'].rstrip())
                con.setdefault(talk['pos_floor'], []).append('</utt>')

                con.setdefault(talk['pos_floor'], []).append('<utt uid="' + str(uids[oid]) + '">')
                con.setdefault(talk['pos_floor'], []).append(talk['ori_message'].rstrip())
                con.setdefault(talk['pos_floor'], []).append('</utt>')
            else:

                floor.append(talk['ori_floor'])
                for fl, v in con.items():
                    if talk['pos_message'].rstrip() in v:
                        con.setdefault(fl,[]).append('<utt uid="' + str(uids[oid]) + '">')
                        con.setdefault(fl,[]).append(talk['ori_message'].rstrip())
                        con.setdefault(fl,[]).append('</utt>')
    for each in con:
        outputFile.write("<s>")
        for sen in con[each]:
            outputFile.write(sen)
        outputFile.write("</s>\n")


    outputFile.write("</dialog>\n")

outputFile.close()
#print(con)
#print(uids)
