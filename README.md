# DM_preprocessing 英文版會使用的部份

#Function sample_match() 中的 wordlist 就是已經切割好的資料 list，
#將英文版的用空格切好的 word list 使用以下函式：
 
#將 wordlist 產生出bigram
chbigram=list2bigram(word_list)

#轉換初統計過frequency的bigram dictionary
bigramfreqdict=bigram2freqdict(chbigram)

#經過sort由大到小排序
bigramfreqsorted=sorted(bigramfreqdict.items(), key=itemgetter(1), reverse=True)

#用來產生edge還有normalized的weight
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

#word_network2.py 中會的 minusNetworks() 使用到sample_match()

# Get edges for the subjective graph
    	edges1 = sample_match(subjPath,"emo")

# Get edges for the objective graph
        edges2 = sample_match(objPath,"all")

#在這裡是因為要做graph相減，若不需要，下方可直接改成
	for edge in edges1:
		value = edges1[edge]
		edges[edge] = value

#下方此兩處可以不需要
	out = codecs.open("network/subjective","w", "utf-8-sig")
	out = codecs.open("network/dropped","w", "utf-8-sig")

#words = {} 和 netEdges = {} 建立完成後，進入 saveNetwork(words,netEdges)，完成gephi input file 製作

