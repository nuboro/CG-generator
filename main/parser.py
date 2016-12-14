#    Copyright (C) 2016 Bror Hultberg
#    Copyright (C) 2016 Joonas Kylmälä

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from streamparser import parse
from streamparser import parse_file


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



def prob(items):
    features=[]  
    for item in items:
        for feature in item:
            features.append(feature) 
    feature_pos = {x:features.count(x)/len(items) for x in features}

    return(feature_pos)

def prepros(filename):
    cohorts = parse_file(open(filename))
    return(cohorts)

def wordclass(cohorts):
    return(get_features(cohorts,lambda x:x.tags[0]))
    
def baseform(cohorts):
    return(get_features(cohorts,lambda x:x.baseform))

def get_features(cohorts,feature): 
    features = []
    for cohort in cohorts:
        posfeatures=set()
        for reading in cohort.readings:
            for subreading in reading:
                posfeatures.add(feature(subreading))
        if posfeatures:
            features.append(list(posfeatures))
    return(features)

def remove_useless(cohorts):
    for cohort in cohorts:
        useless = False
        for reading in cohort.readings:
            for subreading in reading:
                if is_useless(subreading):
                    useless = True
        if not useless:
            yield cohort

def is_useless(subreading):
    useless_tags = ['sent','cm','lquot','rquot','lpar','rpar','guio']
    for tag in subreading.tags:
        if tag in useless_tags:
            return True
    return False

def main():
    corpus_filename = input()
    cohorts = prepros(corpus_filename)
    cohorts = remove_useless(cohorts)

    probabilities = prob(wordclass(cohorts))

    print(probabilities)

main()
