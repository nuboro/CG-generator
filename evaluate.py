# Copyright (C) 2017 Bror Hultberg
#
# This file is part of CG_module.
#
# CG_module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CG_module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.




from streamparser import parse
from parser import wordclass
import subprocess
import collections

x = input()

with open(x, 'r') as data:
    training_data = data.read()

def split_training_data(training_data):
    x=(int(training_data.count("^")/10))
    data=[]
    text=[]
    lines_of_data = training_data.split("\n")


    for i in range(10):
        fraction_of_data=""
        plaintext=""

        if i != 9:
            fraction_of_data = "".join(lines_of_data[i*x:(i+1)*x])
            lexicalUnits = parse(c for c in fraction_of_data)
            for lexicalUnit in lexicalUnits:
                plaintext= plaintext + lexicalUnit.wordform + " "
            data.append(fraction_of_data)
            text.append(plaintext)  
        else:
            fraction_of_data = "".join(lines_of_data[i*x:])
            lexicalUnits = parse(c for c in fraction_of_data)
            for lexicalUnit in lexicalUnits:
                plaintext= plaintext + lexicalUnit.wordform + " "
            data.append(fraction_of_data)
            text.append(plaintext) 
    return(data, text)


data, text = split_training_data(training_data)


def average_ambiguity(option):  #add lambda function
    morphed_text = option
    lexicalUnits = parse(c for c in morphed_text)
    i=0
    ambiguity=0
    for lexicalUnit in lexicalUnits:
        ambiguity=ambiguity+len((lexicalUnit.readings))
        i=i+1
    return(ambiguity/i)

    
def ambiguity_original(text):
    original = subprocess.getoutput('(cd /home/bror/apertium/languages/apertium-kaz/; echo "'+text+'" | lt-proc kaz.automorf.bin |cg-conv -a | vislcg3 --trace -g apertium-kaz.kaz.rlx |cg-conv -A)')
    return(average_ambiguity(original))


def ambiguity_induced(text, induced):
    induced = subprocess.getoutput('(cd /home/bror/apertium/languages/apertium-kaz/; echo "'+text+'" | lt-proc kaz.automorf.bin |cg-conv -a | vislcg3 --trace -g' + induced + '|cg-conv -A)')
    return(average_ambiguity(induced))


def ambiguity_handtagged(handtagged):
    return(average_ambiguity(handtagged))


def count_right_analysis(zip_morphed_vs_handtagged):
    count=0
    for morphed, handtag in zip_morphed_vs_handtagged:
        if (morphed.wordform, morphed.knownness, morphed.readings) == (handtag.wordform, handtag.knownness, handtag.readings):
            count=count+1
    return(count)


def best_ambiguity(ambiguities):
    best = 999999999999999
    index = -1
    for i in range(len(ambiguities)):
        if best > ambiguities[i][1]:
            best = ambiguities[i][1]
            index = i
    return(best, i)



for i in range(10):
    data2 = list(data)
    data2.pop(i)
    training = "".join(data2)

    with open("/tmp/TrainingData"+str(i), 'w') as write:
        write.write(str(training))



    morphed_origal = subprocess.getoutput('(cd /home/bror/apertium/languages/apertium-kaz/; echo "'+text[i]+'" | lt-proc kaz.automorf.bin |cg-conv -a | vislcg3 --trace -g apertium-kaz.kaz.rlx |cg-conv -A)')

    morphed_origal = parse(c for c in morphed_origal)
    handtagged = parse(c for c in data[i])

    morphed_vs_handtagged = zip(morphed_origal, handtagged)



    ambiguity_on_treshold = []
    tresh = 0.00
    while tresh <= 0.15: 
        tresh = tresh + 0.01
        treshold = collections.namedtuple("treshold_and_ambinguity", 'treshold ambiguity_induced')
        cg_file = subprocess.check_output(["python3",'main.py', "/tmp/TrainingData"+str(i), "-t "+ str(tresh)], universal_newlines=True)
        with open("/tmp/Induced_Rules"+str(i), 'w') as write:
            write.write(cg_file)
        morphed_induced = subprocess.getoutput('(cd /home/bror/apertium/languages/apertium-kaz/; echo "' + text[i] + '" | lt-proc kaz.automorf.bin |cg-conv -a | vislcg3 --trace -g '+"/tmp/Induced_Rules"+str(i)+'|cg-conv -A)')
        morphed_induced = parse(c for c in morphed_induced)
        handtagged2 = parse(c for c in data[i])
        induced_vs_handtagged = zip(morphed_induced, handtagged2)
        ambinguity = ambiguity_induced(text[i], "/tmp/Induced_Rules"+str(i) )

        ambiguity_on_treshold.append(treshold(treshold= tresh, ambiguity_induced= ambinguity))

   
    best_average_ambiguity = (best_ambiguity(ambiguity_on_treshold))

    print("EVALUATE ON TEXT " + str(i))
    print("AVERAGE AMBIGUITY ON THE ORIGINAL RULES " + str(ambiguity_original(text[i])))
    print("BEST AVERAGE AMBIGUITY ON THE INDUCED RULES TRESHOLD " + str(best_average_ambiguity[1]) + " AVERAGE " + str(best_average_ambiguity[0]))
    print("AVERAGE AMBIGUITY ON THE HANDTAGGED CORPUS " + str(ambiguity_handtagged(data[i])))
    print("ORIGINAL RULES")
    print(count_right_analysis(morphed_vs_handtagged))
    print("================================================")
    print("INDUCED RULES")
    print(count_right_analysis(induced_vs_handtagged))
    print("\n")























