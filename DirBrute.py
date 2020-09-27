import threading
import urllib.parse
import urllib.error
import urllib.request
import queue
import urllib

threads =100
print("Enter valid target website")
target = input()

wordlist_file = "SVNDigger/all.txt"
resume = None

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/76.0.3809.132 Safari/537.36"

def build_wordlist(wordlist):
	filex = open(wordlist,"r")
	raw = filex.readlines()
#	print("test")
	filex.close()
	found = False
	words = queue.Queue()

	for word in raw:
		word = word.rstrip()

		if resume is not None:
			if found:
				words.put(word)

			else:
				if word == resume:
					found = True
					print("Resumiong wordlist from: %s" %resume)

		else:

			words.put(word)
	return words



def brute(word_queue,extensions=None):
	while not word_queue.empty():
		attempt = word_queue.get()
		list = []
		dot = "."
		if dot not in attempt:
			list.append("/%s/"%attempt)
		else:
			list.append("/%s"%attempt)
		if extensions:
			for ext in extensions:
				list.append("/%s%s"%(attempt,ext))
		for force in list:
			url = "%s%s" % (target,urllib.parse.quote(force))
			try:
				headers = {}
				headers["User-Agent"] = user_agent
				res = urllib.request.Request(url,headers=headers)
				response = urllib.request.urlopen(res)
				if len(response.read()):
					print ("[%d] => %s" % (response.code,url))
			except urllib.error.URLError as e:

				if hasattr(e, 'code') and e.code != 404:
					print ("!!! %d => %s"%(e.code,url))
				pass

word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak",".orig",".inc",".py"]

for i in range(threads):
	t = threading.Thread(target=brute, args=(word_queue,extensions,))
	t.start()







