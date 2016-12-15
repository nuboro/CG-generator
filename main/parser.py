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
from streamparser import parse   #[['vblex', 'n']]
from streamparser import parse_file #[['vblex','vblex'],['n','vblex']]




def combine(a):
    if len(a)==1:
        return([[x] for x in a[0]])
    else:
        return([[x]+y for x in a[0] for y in combine(a[1:])])



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
    list_of_features=combine(wordclass(prepros(x)))
    final_barrier=set()
    for sequence in  list_of_features:
        froz_barrier=bar(sequence,start,end) 
        final_barrier=final_barrier | froz_barrier
    return(final_barrier)



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
        print(cohort.knownness) 
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
        print(subreading)
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
#x=input()
#y=input()
#z=input()
#print(wordclass(prepros(x)))
#print(combine(wordclass(prepros(x))))
#print(barrier(x,y,z))
