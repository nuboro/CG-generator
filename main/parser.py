import sys
from streamparser import parse

def combine(a):
    if len(a)==1:
        return([x for x in a[0]])
    else:
        return([x +' '+ y for x in a[0] for y in combine(a[1:])])



def streamparser(filename):
    try:
        with open(filename, 'r') as data:
            plaintext = data.read()
    except OSError:
        plaintext=filename 
    words=[]
    lexicalUnits = parse(plaintext)
    for lexicalUnit in lexicalUnits:
       words.append('%s (%s) → %s' % (lexicalUnit.wordform, lexicalUnit.knownness, lexicalUnit.readings))
    return(words)


def parser(filename):
    """stores all the possible word class combinations in a list of list  
    """
    words=streamparser(filename)

    wordsclass=[]
    for j in range(len(words)):
       s=set()
       if "streamparser.unknown" in words[j]:
           s.add("unknown")
           wordsclass.append(s)
       else:
            words2=words[j].split("tags=['") 
            for i in range(len(words2)-1):
                words55=words2[i+1][:words2[i+1].index("'")]
                s.add(words55)
            wordsclass.append(s)
    
    finalwc=(combine(wordsclass))
    finalwc2=[]

    for i in range(len(finalwc)):
        m=finalwc[i].split()
        finalwc2.append(m)
    return(finalwc2)


def bar(a,start,end): 
    """returns a set of features(barrier) from list:"a" that occur between string:"start" and string:"end" 
    """
    finalbarrier=set()
    for j in range(len(a)):
        barrier=set()   
        if a[j]==start:
            try: 
                for i in range(len(a)-j+1): 
                    if a[i+j+1] !=end:
                        barrier.add(a[i+j+1])
                    else:
                        froz_barrier=frozenset(barrier) 
                        finalbarrier.add(froz_barrier)
                        break
            except IndexError:
                barrier.clear()
    return(finalbarrier)


def pos(my_list,element):
    indices = [i for i, x in enumerate(my_list) if x == element]
    return(indices)  


def barrier(x,start,end):
    """returns a set of set of features(barrier) from a string/filename(apertium stream format) that occur between string:"start" and string:"end" 
    """ 

    x_parsed=parser(x)
    final=set()
    for sequence in x_parsed:
        froz_barrier=bar(sequence,start,end) 
        final=final | froz_barrier
    return(final)



def prob(cohorts):
    baseforms=[]  
    for cohort in cohorts:
        for baseform in cohort:
            baseforms.append(baseform) 
    word_pos = {x:baseforms.count(x) for x in baseforms}
    for seq in  word_pos:
        word_pos[seq]=word_pos[seq]/len(cohorts)
    return(word_pos)

def prepros(filename):
    try:
        with open(filename, 'r') as data:
            plaintext = data.read()
    except OSError:
        plaintext=filename 
    cohorts = parse(plaintext)
    return(cohorts)
 
def base(filename):
    useless=['sent','cm','lquot','rquot','lpar','rpar','guio']
    baseforms=[]
    cohorts=prepros(filename)
    for cohort in cohorts:
        posbaseforms=set()
        base=[] 
        for reading in cohort.readings:
            for subreading in reading:
                if all(x not in subreading.tags for x in useless):
                    posbaseforms.add(subreading.baseform)
        if posbaseforms:
            baseforms.append(list(posbaseforms))
    return(baseforms)


  
  
def rem_useless(parsed):
    useless=['streamparser.unknown',"tags=['sent']","tags=['cm']","tags=['lquot']","tags=['rquot']","tags=['lpar']","tags=['rpar']", "tags=[\'apos\']", "tags=['guio']" ]
    parsed_useful = [item for item in parsed.reading if not any([x in item for x in useless]) ]
    return(parsed_useful)




x=input()

print(prob(base(x)))


