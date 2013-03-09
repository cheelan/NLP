def getScore(targetdef,featuredef):
	#assume that each input is a string
	featureNextWord= "";
	targetNextWord= "";
	fWordList = featuredef.split(" ")
	tWordList = targetdef.split(" ")
	fWordCounter=0;
	score=0;
	tWordCounter=0;
	retain=0;
	checkWordsCount=0;
	while (tWordCounter < len(tWordList)):
		while (fWordCounter < len(fWordList)):
			if tWordList[tWordCounter] == fWordList[fWordCounter]:
				featureNextWord= fWordList[fWordCounter];
				targetNextWord= tWordList[tWordCounter];
				while(targetNextWord == featureNextWord):
					checkWordsCount =checkWordsCount + 1;
					fWordCounter = fWordCounter + 1
					tWordCounter = tWordCounter + 1
					if fWordCounter>=len(fWordList):
						break
					featureNextWord= fWordList[fWordCounter];
					targetNextWord = tWordList[tWordCounter];
				score = score+ (2)**checkWordsCount;
				checkWordsCount=0;
			else:
				fWordCounter = fWordCounter + 1;
			tWordCounter= retain;
		fWordCounter=0;
		retain =retain +1;
		tWordCounter= retain;
	print(score)

getScore("a b c d e", "b b c a f")
getScore("a b c d e", "b b c a f c d e")
getScore("a","a")
getScore("a","b")
getScore("a","")
getScore("a","sdsg a")