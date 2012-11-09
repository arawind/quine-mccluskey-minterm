n=0
orArray=[]
def main():
  n=input('Enter number of implicants')
  andArray=[]
  orArray=[]
  for i in range(0,n):
    orArray = input('Enter or terms for ')
    orArray = list(set(orArray))
    orArray.sort()
    if orArray not in andArray:
       andArray.append(orArray)
  andArray2=andArray
  print andArray
  def removeY(array):     #remove terms which are in the form of X+XY from orArray structures, array parameter must be [[1,2],[1,2,5,6]]
    array2=[]
    for i in range(0,len(array)):
       x=array[i]
       for j in range(i+1,len(array)):
          xy=array[j]
          xset = set(x)
          xyset = set(xy)
          intxxy = xset.intersection(xyset)
          if intxxy==xset:
             #print 'a'
             #print xy
             array2.append(xy)
          elif intxxy==xyset:
             #print 'b'
             array2.append(x)

    for x in array2:
       if x in array:
         array.remove(x)
    return array


#Multiply
  def multiply(andArray):
    finalArray=[]
    for i in range(0,len(andArray),2):
      x=andArray[i]
      #print i
      if (i+1)<len(andArray):
         y=andArray[i+1]
      temp=[]
      tempArray=[]
      for a in x:
        for b in y:
          al=isinstance(a,list)
          #print a
          #print al
          bl=isinstance(b,list)   #is 'a' a list?
          #print b
          #print bl
          if al and bl:
             temp=list(a+b)
          elif al and not bl:
             temp=list(a)
             temp.append(b)
          elif bl and not al:
             temp=list(b)
             temp.append(a)
          elif not al and not bl:
             temp=[]
             temp.append(a)
             temp.append(b)
          temp = list(set(temp))
          temp.sort()
          #print temp
          if temp not in tempArray:
             tempArray.append(temp)
      tempArray=removeY(tempArray)
      for i in range(0,len(tempArray)):
         elem = tempArray[i]
         if len(elem)==1:
            tempArray[i]=elem[0]

      finalArray.append(tempArray)
    andArray=finalArray 
#if len(andArray)>1:
#    multiply(andArray)
    #print andArray
    return andArray
  while len(andArray)>1:  
    andArray = multiply(andArray)
    print andArray
if __name__ == '__main__':
  main()
