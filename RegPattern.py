# -*- coding: utf-8 -*- 
import re



class RegPattern(object):
	"""docstring for RegPattern"""
	def __init__(self):
		super(RegPattern, self).__init__()
		# self.arg = arg

	'''
	patterns
	'''
	re_ex = r'!{1}' #exclamation
	re_mutiex = r'!{2,20}'
	re_dot = r'\.{2,20}' # dot, appear more than twice
	re_que = r'\?{2,20}' # question mark, appear more than twice
	re_ch = r'([a-zA-Z])(\1+)' # repeated letters appear more than once
	# re_ch = r'([a-zA-Z])\1+'
	#re_chinese = u"[\u4e00-\u9fa5]{1}|[\u0021-\uff65\u2000-\u206f\u3000-\u303f\ufb00-\ufffd]{1}" #單一中文字
	#re_chinese = ur"[\u4e00-\u9fa5]{1}|[\u0021-\u30fb\ua4fe-\uabeb\u2000-\u206f\u3000-\u303f\ufb00-\ufffd]{2,20}|[\u3100-\u312F]{2,20}|[\u3100-\u312F]{1}|[\u0021-\u30fb\ua4fe-\uabeb\u2000-\u206f\u3000-\u303f\ufb00-\ufffd]{1}|." #中文+英文+標碘+標碘表情符號
	re_chinese = ur"<user_name>|<hash_tag>|<emoji>|(?:[A-Z]\.)+[A-Z]?|[a-zA-Z]+\'[a-zA-Z]{1}|[a-zA-Z]+|[ㄅ-ㄩˊ-˙]+|."
	
	'''
	emoticon
	the emoticons come from https://en.wikipedia.org/wiki/List_of_emoticons
	metacharacters: . ^ $ * + ? { } [ ] \ | ( )
	'''
	re_happy = r"(:-\)|:\)|:D|:o\)|:\]|:3|:c\)|:>|=\]|8\)|=\)|:\}|:\^\)|:-\)\))" # :‑) :) :D :o) :] :3 :c) :> =] 8) =) :} :^) :-))
	re_laugh = r"(:‑D|8‑D|8D|x‑D|xD|X‑D|XD|=‑D|=D|=‑3|=3|B\^D)" # :‑D 8‑D 8D x‑D xD X‑D XD =‑D =D =‑3 =3 B^D	
	re_sad = r"(>:\[|:‑\(|:\(|:‑c|:c|:‑<|:<|:‑\[|:\[|:\{|;\()" # >:[ :‑( :( :‑c :c :‑< :っC :< :‑[ :[ :{
	re_angry = r"(:-\|\||:@|>:\()" # :-|| :@ >:(
	re_cry = r"(:'‑\(|:'\()" # :'‑( :'(
	re_horror = r"(D:<|D:|D8|D;|D=|DX|v\.v|D‑':)" # D:< D: D8 D; D= DX v.v D‑':
	re_surprise = r"(>:O|:‑O|:O|:‑o|:o|8‑0|O_O|o‑o|O_o|o_O|o_o|O-O)" # >:O :‑O :O :‑o :o 8‑0 O_O o‑o O_o o_O o_o O-O
	re_love = r"(:\*|:-\*|:\^\*|\( '\}\{'\))" # :* :-* :^* ( '}{' )
	re_wink = r"(;‑\)|;\)|\*-\)|\*\)|;‑\]|;\]|;D|;\^\)|:‑,)" # ;‑) ;) *-) *) ;‑] ;] ;D ;^) :‑,
	re_uneasy = r"(>:\\\\|>:/|:‑/|:‑\.|:/|:\\\\|=/|=\\\\|:L|=L|:S|>\.<)" # >:\ >:/ :‑/ :‑. :/ :\ =/ =\ :L =L :S >.<
	re_trouble = r"(\(>_<\)|\(>_<\)>)" # (>_<) (>_<)>


	'''
	words, punctuations and emoticons
	'''
	#re_all = r"[\w']+|[.,!?;]{2,20}|[.,!?;]|<PERSON>|<URL>|:-\)|:\)|:D|:o\)|:\]|:3|:c\)|:>|=\]|8\)|=\)|:\}|:\^\)|:-\)\)|:‑D|8‑D|8D|x‑D|xD|X‑D|XD|=‑D|=D|=‑3|=3|B\^D|>:\[|:‑\(|:\(|:‑c|:c|:‑<|:<|:‑\[|:\[|:\{|;\(|D:<|D:|D8|D;|D=|DX|v\.v|D‑':|>:O|:‑O|:O|:‑o|:o|8‑0|O_O|o‑o|O_o|o_O|o_o|O-O|:\*|:-\*|:\^\*|\( '\}\{'\)"
	re_all = r"[.,!?;]{2,20}|[.,!?;]|<PERSON>|<URL>|:-\)|:\)|:D|:o\)|:\]|:3|:c\)|:>|=\]|8\)|=\)|:\}|:\^\)|:-\)\)|:‑D|8‑D|8D|x‑D|xD|X‑D|XD|=‑D|=D|=‑3|=3|B\^D|>:\[|:‑\(|:\(|:‑c|:c|:‑<|:<|:‑\[|:\[|:\{|;\(|D:<|D:|D8|D;|D=|DX|v\.v|D‑':|>:O|:‑O|:O|:‑o|:o|8‑0|O_O|o‑o|O_o|o_O|o_o|O-O|:\*|:-\*|:\^\*|\( '\}\{'\)"


	'''
	re_ex: 單個感嘆號
	re_multiex: 兩個及兩個以上感嘆號
	re_dot: 三個及三個以上句號
	re_que: 兩個及兩個以上問號
	re_ch: 重複出現三次以上的字母
	re_all: 匹配全部
	'''
	def get_pattern(self, text, re_text):
		if re_text == 're_ex':
			return self.__get_ex(text)
		elif re_text == 're_multiex':
			return self.__get_multiex(text)
		elif re_text == 're_dot':
			return self.__get_dot(text)
		elif re_text == 're_que':
			return self.__get_que(text)
		elif re_text == 're_ch':
			return self.__get_ch(text)
		elif re_text == 're_all':
			return self.__get_all(text)
		elif re_text == 're_chinese':
			return self.__get_chinese(text)

	def __get_ex(self, text):
		p = re.compile(self.re_ex)
		match = p.findall(text)
		return len(match)

	def __get_multiex(self, text):
		p = re.compile(self.re_mutiex)
		match = p.findall(text)
		return len(match)

	def __get_dot(self, text):
		p = re.compile(self.re_dot)
		match = p.findall(text)
		return len(match)

	def __get_que(self, text):
		p = re.compile(self.re_que)
		match = p.findall(text)
		return len(match)

	def __get_ch(self, text):
		count = 0
		p = re.compile(self.re_ch)
		match = p.findall(text)
		for m in match:
			if len(m[1]) > 1:
				count += 1
		return count

	# return the match list rather than the count of matched items
	def __get_all(self, text):
		match = []
		p = re.compile(self.re_all)
		match = p.findall(text)
		return match

	def __get_chinese(self, text):
		match = []
		p = re.compile(self.re_chinese)
		match = p.findall(text)
		return match
		#p = re.sub(self.re_chinese,"",text)
		#return p

	def is_starts_with_hashtag(self, item):

		pattern = r"\#"

		return re.match(pattern, item)



	def is_starts_with_url(self, item):

		pattern = r"http"

		return re.match(pattern, item)



	def is_starts_with_at(self, item):

		pattern = r"@"

		return re.match(pattern, item)



	def is_starts_with_text(self, item):

		#if self.is_starts_with_hashtag(item) or self.is_starts_with_at(item) or self.is_starts_with_url(item):
		#
		#	return False
		#
		#else:
		return True

	def combine_punct(self, word_list):
		result = []
		punct_pat = r'^[〜~～。、・！？!?【】《》“”『』,.。、…]+$'
		punct_str = ""
		#for char in word_list:
		for index, char in enumerate(word_list):
			#if index == 0:
			#	result.append(char)
			#	continue
			if re.match(punct_pat, char):
				punct_str += char
			else:
				if punct_str != "":
					result.append(punct_str)
					punct_str = ""
				result.append(char)
		if punct_str != "":
			result.append(punct_str)
		return result

	def combine_num_and_eng(self, word_list):
		result = []
		num_pat = r'^[0-9０-９]+(,[0-9０-９]+)?$|^[0-9０-９]+(\.[0-9０-９]+)?$'
		num_pun = r'^[\.|%]{1}'
		eng_pat = r'^[a-zA-Z]+$'
		num_str = ""
		flag = 0
		for index, char in enumerate(word_list):
			#if char == "":
			#	continue
			#if index == 0:
			#	result.append(char)
			#	continue
			if re.match(num_pat, char): # If number, put is in num_str
				num_str += char
			elif re.match(num_pun, char) and num_str != "": # If number + \., make it as one item
				num_str += char
				if char == "%":
					result.append(num_str)
					num_str = ""
				flag = 1
			#elif re.match(eng_pat, char) and num_str != "": # If number + English, make it as one item
			#	num_str += char
			#	result.append(num_str)
			#	num_str = ""
			else: # If not the combination above
				if num_str != "":
					result.append(num_str)
					num_str = ""
				result.append(char)
		if num_str != "":
			result.append(num_str)
		return result
	

	def combine_emoticons(self, word_list):
		excp_list = ["「」","」「","()","（）","）（",")(",":「","：「",":[",")「","）「"]
		excp_pattern = ur'[」\)）]{1}[+＋]?[「\(（]{1}'
		excp_pattern_2 = ur'[「\(（]{1}[」\)）]{1}|[」\)）]{1}[「\(（]{1}|[」\)）]{1}[」\)）]{1}|[「\(（]{1}[「\(（]{1}|[」\)）]{1}.|.[」\)）]{1}'
		result = []
		pattern_non_emoticon = ur'<user_name>|<hash_tag>|<emoji>|[a-zA-Z]{2,}|[一-龥0-9０-９。，、ー〜，~～！？【】《》“”『』!?…・\,\.]|[ㄅ-ㄩˊ-˙]+'
		emoticon_str = ""
		for char in word_list:
			if self.is_starts_with_text(char):
				if re.match(pattern_non_emoticon, char) != None: # If not a part of emoticon
					if emoticon_str != "":
						i = len(emoticon_str) - 1
						if emoticon_str[i] == " " or emoticon_str[i] == "　":
							while i >= 0:
								if emoticon_str[i] == " " or emoticon_str[i] == "　":
									result.append(emoticon_str[i])
									i -= 1
								else:
									break
							emoticon_str = emoticon_str[:i+1]
							result.append(emoticon_str)
							#p = re.compile(excp_pattern)
							#if p.findall(emoticon_str):#
							#	for j in range(0,len(emoticon_str),1):
							#		result.append(emoticon_str[j])
							#else:
							#	result.append(emoticon_str)
						else:
							result.append(emoticon_str)
						emoticon_str = ""
					result.append(char)
				else: # If a part of emoticon
					if emoticon_str == "" and (char ==" " or char == "　"):
						result.append(char)
					else:
						emoticon_str += char
					if len(emoticon_str) == 2:
						#for item in excp_list:
						p = re.compile(excp_pattern_2)
						if p.findall(emoticon_str):#
							for j in range(0,len(emoticon_str),1):
								result.append(emoticon_str[j])
							emoticon_str = ""
			else: # If start with #, @, http or others
				if emoticon_str != "":
					result.append(emoticon_str)
					emoticon_str = ""
				#result.append(char)   here
		if emoticon_str != "":
			result.append(emoticon_str)
		return result

