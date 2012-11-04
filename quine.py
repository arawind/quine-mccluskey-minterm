#Quine McKluskey Algorithm
#Implemented by Aravind Pedapudi
#http://arawind.com

mintermArray=input("Enter minterms seperated by a \',\'") #minterms as an array

mintermArray=list(set(mintermArray));
mintermArray.sort();

#parse minterms, find number of bits
numBits=0
maxMinterm=max(mintermArray)
columns=[]
decArray=[]
while maxMinterm/(2**numBits) !=0:
    numBits+=1
binArrays=[]

#init binary terms
binArray=[0 for x in range(0,len(mintermArray))]
j=0
#binaryTerms
while j<len(mintermArray):
    i=0
    decArray.append([mintermArray[j]])
    binArray[j]=[0 for x in range(0,numBits)]
    while i<numBits:
        binArray[j][i] += (mintermArray[j]>>(numBits-1-i))&1
        i+=1
    binArray[j]=''.join(map(str,binArray[j]))
    j+=1

#add to binArrays
binArrays.append(binArray)

#minterms object, has column number, numOnes, tick and bits in array form
class minterm:
    column=0
    numOnes=0
    tick=0
    bits=[]
    decimals=[]
    def getNumOnes(self,term):
        return (term).count('1')    
    def __init__(self,term,column,decimals):
        self.decimals=[]
        self.bits=term
        self.column=column
        self.numOnes=self.getNumOnes(term)
        self.decimals.append(decimals)

#groups object
class groups:
    columnNum=0
    terms=[]
    numOnes=0
    def __init__(self,ones):
        self.terms=[]
        self.numOnes=ones
    def add(self,term):
        self.terms.append(term)        

#columns object
class column:
    columnNum=0
    terms=[]
    groupArray=[]
    numTerms=0
    def __init__(self,column):
        self.columnNum=column
        i=0
        self.groupArray=[]
        while i<=numBits:
            self.groupArray.append(groups(i))
            i+=1
    def addElement(self,term):
        self.terms.append(term)
        self.numTerms+=1
        self.groupArray[term.numOnes].add(term)        

#
def checkOnes(term1,term2):
    ok=False
    i=0
    numDifferences=0
    while i<numBits:
        if(term1.bits[i]!=term2.bits[i]):
            numDifferences+=1
            if(numDifferences==1):
                #print "%s" % numDifferences
                #print "%s" % i
                ok=i+1 #extra one to escape the 0=false condition
            
                
        i+=1
    if numDifferences!=1:
        ok=False
    return ok

for columnNumber in range(0,20):
    #making column0
    columns.append(column(columnNumber))
    for x in range(0,len(binArrays[columnNumber])):
        y=binArrays[columnNumber][x]
        columns[columnNumber].addElement(minterm(y,columnNumber,decArray[x]))

    binArray=[]
    decArray=[]
    combinations=False
    for i in range(0,len(columns[columnNumber].groupArray)):
        group1 = columns[columnNumber].groupArray[i]
        for j in range(i+1,len(columns[columnNumber].groupArray)):
            group2 = columns[columnNumber].groupArray[j]
            #print("g1ones %s" % group1.numOnes)
            #print("g2ones %s" % group2.numOnes)
            if(group2.numOnes-group1.numOnes!=1):
                continue
            else:
                for p in range(0,len(group1.terms)):
                    element1=group1.terms[p]                                    
                    for q in range(0,len(group2.terms)):
                        element2=group2.terms[q]
                        bitNum=checkOnes(element1,element2)
                        #print(binArray)
                        if bitNum:
                            combinations=True
                            bitNum-=1 #removing the extra one we added back there
                            element1.tick=1
                            element2.tick=1
                            tempDec=[]
                            for x in element1.decimals:
                                if isinstance(x,list):
                                    for y in x:
                                        tempDec.append(y)
                                else:
                                    tempDec.append(x)
                            for x in element2.decimals:
                                if isinstance(x,list):
                                    for y in x:
                                        tempDec.append(y)
                                else:
                                    tempDec.append(x)
                                                    
                            #tempDec.sort()
                            
                            
                            tempbits= list(element1.bits)
                            tempbits[bitNum]='-'
                            tempbits = "".join(tempbits)
                            binArray.append(tempbits)

                            decArray.append(tempDec)
                            #print(tempDec)
    binArrays.append(binArray)
    if not combinations:
        #print(columnNumber)
        break


#display
for x in columns:
    print 'Column: %s' %x.columnNum
    for y in x.groupArray:
        if(len(y.terms)>0):
            print '-----------------------------------------------------------' 
        for z in y.terms:
            print '%15s %10s %10s' % (','.join(map(str,z.decimals[0])),z.bits,z.tick)


##            #making column1 and probably iterate this over and over                        
##            columns.append(column(1))
##            for x in binArrays[1]:
##                #print(x)
##                columns[1].addElement(minterm(x,1))
                    
    











