#Quine McCluskey Algorithm
#Implemented by Aravind Pedapudi
#http://arawind.com

import petricks

mintermArray=input("Enter minterms seperated by a \',\': ") #minterms as an array
dcYorN=raw_input('Don\'t care terms? (y/N) ')
dontCareArray=[]
if dcYorN or dcYorN=='y' or dcYorN=='Y':
  dontCareArray = input("Enter donot care terms sep by a \',\'") #dontcare terms

mintermArray=list(set(mintermArray))
mintermArray.sort()

dontCareArray =list(set(dontCareArray))
dontCareArray.sort()

#check for errors

#error1: term will take dontCareArray as a higher preference if it exists in both mintermArray and dontCareArray
mintermArray= list(set(mintermArray).difference(dontCareArray))
#print mintermArray
#end errors

#print mintermArray
#print dontCareArray
mintermArray = list(set(mintermArray+dontCareArray))
mintermArray.sort()
#print mintermArray;
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
    dontCare=False
    def getNumOnes(self,term):
        return (term).count('1')    
    def __init__(self,term,column,decimals,dcare):
        decimals.sort()
        self.decimals=[]
        self.bits=term
        self.column=column
        self.numOnes=self.getNumOnes(term)
        self.decimals.append(decimals)
        self.dontCare=dcare
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
        dcare=True
        for elem in decArray[x]:    #decArray is an array with elements like this [1,2,5,7] or [4]
            if elem not in dontCareArray:
                dcare=False
        columns[columnNumber].addElement(minterm(y,columnNumber,decArray[x],dcare))
        # print decArray[x]

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
                            tempDec.sort()
                            tempbits= list(element1.bits)
                            tempbits[bitNum]='-'
                            tempbits = "".join(tempbits)
                            #print tempDec
                            if tempDec not in decArray:
                                binArray.append(tempbits)
                                decArray.append(tempDec)
                            #print(tempDec)
    binArrays.append(binArray)
    if not combinations:
        #print(columnNumber)
        break


##################### make table for prime implicants
mintermArrayWdc= list(set(mintermArray).difference(dontCareArray)) #to get minterms without dont care terms
#those will be your columns
primeImplicants=[]
for x in columns:
    for y in x.groupArray:
        for z in y.terms:
            if (not z.dontCare) and (not z.tick):
                primeImplicants.append(z)
###### essential prime implicants
essentialPrimePos=[]
i=0
columnCover=[0 for x in range(0,len(mintermArrayWdc))]
j=0
primeImplicantPos=[]
for x in mintermArrayWdc:
    i=0
    temp=[]
    for y in primeImplicants:
        if x in y.decimals[0]:
           temp.append(i)   
        i=i+1
    columnCover[j]=list(temp)
    if len(columnCover[j])==1:
       essentialPrimePos.append(columnCover[j][0])
    else:
       primeImplicantPos.append(list(columnCover[j]))
    j=j+1  

petrick = petricks.init(primeImplicantPos)
finalArray = petrick.finalArray[0]
def lenMapper(array):
    if not isinstance(array,list):
       return 1
    else:
       return len(array)
lengthOfFinalArray=map(lenMapper,finalArray)
minLength=min(lengthOfFinalArray)
minimals=[]
for i in finalArray:
    if isinstance(i,list):
       if len(i)==minLength:
          minimals.append(i)
    else:
       temp=[]
       temp.append(i)
       minimals.append(list(temp))

####multiple solutions
solutions=[]
for minimal in minimals:
    solution=[]
    for espos in essentialPrimePos:
        solution.append(primeImplicants[espos])

    for pos in minimal:
        solution.append(primeImplicants[pos])
    solutions.append(solution)


print ''
#display
for x in columns:
    print 'Column: %s' %x.columnNum
    for y in x.groupArray:
        if(len(y.terms)>0):
            print '-----------------------------------------------------------' 
        for z in y.terms:
            print '%15s %10s %10s %10s' % (','.join(map(str,z.decimals[0])),z.bits,'+' if z.tick else '-','D' if z.dontCare  else '-')
            
print ''

print 'Prime Implicants Table: '
print '-----------------------------------------------------------' 
print '%15s %10s' % ('',''), 
for minterm in mintermArrayWdc:
    print '%5s'%(minterm), 
print('')
i=0
for x in primeImplicants:
    print '%15s %10s' % (','.join(map(str,x.decimals[0])), x.bits),
    for j in range(0,len(mintermArrayWdc)):
        if i in columnCover[j]:
           print '%5s'%('x'),
        else:
           print '%5s'%(''),
    i=i+1
    print ''
print ''
print 'Removing Essential Prime Implicants'
print '-----------------------------------------------------------' 
print '%15s %10s' % ('',''), 
for j in range(0,len(mintermArrayWdc)):
  if len(columnCover[j])>1:
     print '%5s'%(mintermArrayWdc[j]),
  else:
     print '',
print('')
i=0
for x in primeImplicants:
    print '%15s %10s' % (','.join(map(str,x.decimals[0])), x.bits),
    for j in range(0,len(mintermArrayWdc)):
        if i in columnCover[j]:
           print '%5s'%('x'),
        else:
           print '%5s'%(''),
    i=i+1
    print ''
##Show Solutions
print ''
print ''
if len(solutions)>1:
  print 'Solutions:'
else:
  print 'Solution:'
print '-----------------------------------------------------------' 
i=0
alphabets=[chr(code) for code in range(ord('a'),ord('z'))]
solutionAlphs=[]
for solution in solutions:
    print 'Solution #%d'%(i+1)
    alphTerms=[]
    for term in solution:
        alphTerm = []
        for j in range(0,numBits):
            if term.bits[j] == '1':
               alphTerm.append(alphabets[j])
            elif term.bits[j] == '0':
               alphTerm.append(alphabets[j]+'\'')
            elif term.bits[j]=='-':
               pass
        alphTerms.append(''.join(alphTerm))
    print "%s" %(' + '.join(map(str,alphTerms)))
    print ''
    i=i+1
    solutionAlphs.append(alphTerms)

##            #making column1 and probably iterate this over and over                        
##            columns.append(column(1))
##            for x in binArrays[1]:
##                #print(x)
##                columns[1].addElement(minterm(x,1))
