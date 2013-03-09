import sys, itertools, copy, random, nltk.tokenize, os, re, math

class Scores:
    #n = 0
    #dictionary = None
    #count_list = [0]
    #vocab = set()

    #n: number of grams (1 = unigram, 2 = bigram, etc.)
    #text: a text corpus to model
    #smoothingBound: smooth all words that appear less than the smoothingBound
    #Returns a dictionary with keys that strings representing lists of words, and values that are counts
    #TO-DO: Punctuation (find and replace should do the trick)
    def __init__(self):
        print 'hi'

    def getScore(self, targetSense, featureSense):
        consecutive = 0		# running number of consecutive overlaps
        targetList = targetSense.split(' ')
        featureList = featureSense.split(' ')
        targetIndex = 0
        score = 0
        baseScore = 2

        while targetIndex<len(targetList):
            if targetFeature in featureList:
                start = targetIndex
                checkIndex = featureList.index(targetList[targetIndex]) + 1
                targetIndex+=1
                consecutive = 1
                while checkIndex<len(featureList):		# second run finds all remaining matches of targetFeature in featureList
                    if checkTargetIndex>=len(targetList):
                        #add sub-score here
                        score+=baseScore**consecutive
                        checkTargetIndex=start
                        consecutive = 0
                    else:
                        if featureList[checkIndex]==targetList[checkTargetIndex]:
                            consecutive+=1
                            checkTargetIndex+=1
                            checkIndex+=1
                        else:
                            #add sub-score here
                            #does there need to be a case where consecutive==0 because it should just be 0/1??
                            #resolved?
                            if consecutive==0:
                                checkIndex+=1
                            else:
                                #add sub-score here
                                score+=baseScore**consecutive
                                consecutive=0
                                checkTargetIndex=start
        return score

'''
			targetFeature = targetList[targetIndex]
			start = targetIndex
			targetIndex+=1
			
			if targetFeature in featureList:
				checkIndex = featureList.index(targetFeature) + 1
				consecutive=1
				while checkIndex<len(featureList) && targetIndex<len(targetList):			# first run that changes targetIndex
					if featureList[checkIndex]==targetList[targetIndex]:
						consecutive+=1
						targetIndex+=1
						checkIndex+=1
					else:
						break
				#add sub-score to running score
				consecutive=0
				checkTargetIndex = start
				
				while checkIndex<len(featureList) && checkTargetIndex<len(targetList):		# second run finds all remaining matches of targetFeature in featureList
					if featureList[checkIndex]==targetList[checkTargetIndex]:
						consecutive+=1
						checkTargetIndex+=1
						checkIndex+=1
					else:
						#add sub-score here
						#does there need to be a case where consecutive==0 because it should just be 0/1??
						
						if consecutive==0:
							checkIndex+=1
						else:
							consecutive=0
							checkTargetIndex=start'''

s = Scores()
print s.getScore('a b c d e', 'b b c a f')
