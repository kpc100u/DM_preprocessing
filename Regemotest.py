# -*- coding: utf-8 -*-
from nltk.util import ngrams
import nltk
import codecs
import unicodedata
import operator
import re
import json
from os import listdir
from os.path import isfile, join
import sys
from multiprocessing import Process
import RegPattern
from operator import itemgetter

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def remove_control_characters(s):
	return u"".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def load( path):
	words = {}
	f = codecs.open(path,"r", "utf-8")
	for word in f:
		word = word.split("\t")[0]
		word = remove_control_characters(word)
		words[word.strip()] = word.strip()
	print "Loaded %s words"%str(len(words))
	return words

def removeURL(tweet):
	url_patt = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
	tweet = re.sub(url_patt, '', tweet)
	return tweet
def removeHashTag(tweet):
	hash_patt = ur'#([a-zA-Z]+|[一-龠]+)'
	tweet = re.sub(hash_patt, "<hash_tag>", tweet)
	return tweet

def removeEMOJI(tweet,emoji):
	#emoticon = ":-)|:)|:D|:o)|:]|:3|:c)|:>|=]|8)|=)|:}|:^)|:-))|:‑D|8‑D|8D|x‑D|xD|X‑D|XD|=‑D|=D|=‑3|=3|B^D|>:[|:‑(|:(|:‑c|:c|:‑<|:<|:‑[|:[|:{|;(|D:<|D:|D8|D;|D=|DX|v.v|D‑':|>:O|:‑O|:O|:‑o|:o|8‑0|O_O|o‑o|O_o|o_O|o_o|O-O|:*|:-*|:^*|( '}{')"
	#emoticon_list = emoticon.split("|")
	result_dict = {}
	result_list = []
	line = tweet
	#print tweet
	for key, value in emoji:
		if key in tweet and len(key) > 1:
			#print key
			index = 0
			#for m in re.finditer(key, tweet):
			while index < len(line):
				index = line.find(key, index)
				#print index
				if index == -1:
					break
				#index += len(key)
				result_dict[index] = unicode(key)
				index += len(unicode(key))
				#print len(line)
				#print len(key)
			tweet = tweet.replace(key,"<emoji>")
	result_dict = sorted(result_dict.items(), key=itemgetter(0))
	#print result_dict
	for key, value in result_dict:
		result_list.append(value)
	return tweet, result_list

def load_list(path,path2):
	emoticon = "♪(^o^)v|（ ￣口￣)/|(^口^)|*\(^o^)/*|(^0^)|(⊙ˍ ⊙)|Σ(｡>艸<｡)|(*@?@*)|(^~ ^)|(^~^)|~(^0^)~|*(^!^)*|(^0 ^)|(^~ ^)|(^ з^)|←_←|⊙_⊙|ˊ_>ˋ|:-)|：－）||:)|：）|:D|：Ｄ|:o)|：ｏ）|:]|：〕|:3|：３|:c)|：ｃ|:>|：＞|=]|＝〕|8)|８）|=)|＝）|:}|：｝|:^)|：︿）|:-))|：－））|:‑D|：－Ｄ|8‑D|８－Ｄ|8D|８Ｄ|x‑D|ｘ－Ｄ|xD|ｘＤ|X‑D|Ｘ－Ｄ|XD|ＸＤ|=‑D|＝－Ｄ|=D|＝Ｄ|=‑3|＝－３|=3|＝３|B^D|Ｂ︿Ｄ|>:[|＞：〔|:‑(|：－（|:(|：（|:‑c|：－ｃ|:c|：ｃ|:‑<|：－＜|:<|：＜|:‑[|：－〔|:[|：〔|:{|：｛|;(|；（|D:<|Ｄ：＜|D:|Ｄ：|D8|Ｄ８|D;|Ｄ；|D=|Ｄ＝|DX|ＤＸ|v.v|ｖ．ｖ|D‑':|Ｄ－’：|>:O|＞：Ｏ|:‑O|：－Ｏ|:O|：Ｏ|:‑o|：－ｏ|:o|：ｏ|8‑0|８－０|O_O|ＯˍＯ|o‑o|ｏˍｏ|O_o|Ｏˍｏ|o_O|ｏˍＯ|o_o|ｏˍｏ|O-O|Ｏ－Ｏ|:*|：＊|:-*|：－＊|:^*|：︿＊|( '}{')|（　’｝｛’）|@@|＠＠"
        emoticon_list = emoticon.split("|")
	f = codecs.open(path,"r", "utf-8")
	f2 = codecs.open(path2,"r", "utf-8")
	XD_str = f2.read()
	XD_list = XD_str.split("\n")
	emo_list = json.loads(f.read())
	emo_dict = {}
	f.close()
	f2.close()
	for item in emo_list:
		emo_dict[item] = len(unicode(item))
	for item in emoticon_list:
		emo_dict[item] = len(unicode(item))
	for item in XD_list:
		emo_dict[item] = len(unicode(item))
	emo_dict = sorted(emo_dict.items(), key=itemgetter(1),reverse = True)
	#print emo_dict
	return emo_dict

def sample_match(emoPath,meta):
	edges = {}
	print "Processing "+emoPath

	content_file = codecs.open(emoPath,"r",encoding='utf-8')
	out = codecs.open("./network/patterns/samples/30/samples_"+meta,"w", "utf-8-sig")
	emoji = load_list("./emo_list.txt","./XD_list.txt")#
	word_list = []
	#for line in jsonContent:
	for line in content_file:
		line = remove_control_characters(line.strip())
		#print line
		#s = unicode(line)
		line = removeURL(line)
		line = removeHashTag(line)
		emoji_result = []#
		line, emoji_result = removeEMOJI(line,emoji)#
		
		r = RegPattern.RegPattern()
		result = r.get_pattern(line,"re_chinese")
		result = r.combine_num_and_eng(result)
		result = r.combine_punct(result)
		result = r.combine_emoticons(result)
		#print result
		i = 0
		if len(result) != 0:
			#out.write(result)
			#out.write("\n")
			for item in result:
				if item == "<emoji>":
					#print emoji_result
					#print item
					word_list.append(emoji_result[i])
					out.write(emoji_result[i])
					i+=1
					out.write("\n")
				else:	
					word_list.append(item)
					#print word_list
					out.write(item)
					out.write("\n")
			#for x in result:
			#	word_list.append(x.encode('utf-8'))
			#print word_list
	chfreqdict=list2freqdict(word_list)
	chfreqsorted=sorted(chfreqdict.items(), key=itemgetter(1), reverse=True)
	#print chfreqsorted
	chbigram=list2bigram(word_list)
	#print word_list
	if(meta == "2"):
		return chbigram
	#print chbigram
	bigramfreqdict=bigram2freqdict(chbigram)
	bigramfreqsorted=sorted(bigramfreqdict.items(), key=itemgetter(1), reverse=True)
	#print bigramfreqsorted

	maxi = 0.0
	foundMax = 0
	for (token,num) in bigramfreqsorted:
		if len(token[0]) != 0 and len(token[1]) != 0:
			if token[0] == " ":
				w1 = "_blank_"
			else:
				w1 = token[0]
			if token[1] == " ":
				w2 = "_blank_"
			else:
				w2 = token[1]
			if not foundMax:
				foundMax = 1
				maxi = float(num)
			#out.write("%s -> %s : %d - %f"%(token[0],token[1],num, float(num)/float(maxi)))
			#out.write("\n")
			edges["%s\t%s"%(w1,w2)]=float(num)/float(maxi)
	out.close()
	return edges;
			

def list2freqdict(mylist):
	mydict=dict()
	for ch in mylist:
		mydict[ch]=mydict.get(ch,0)+1
	return mydict

def list2bigram(mylist):
	return [mylist[i:i+2] for i in range(0,len(mylist)-1)]

def bigram2freqdict(mybigram):
	mydict=dict()
	for (ch1,ch2) in mybigram:
		mydict[(ch1,ch2)]=mydict.get((ch1,ch2),0)+1
	return mydict

def replace_space(path):
	with codecs.open(path,"r", "utf-8") as content_file:
		content = content_file.read()
	print content
	content.replace(" ","_blank_")
	out = codecs.open("path","w", "utf-8-sig")
	out.write(content)
	out.close()



#sample_match("./network/test","test")
#replace_space("./network/patterns/samples/30/samples")
