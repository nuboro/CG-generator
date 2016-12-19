#    Copyright (C) 2016 Bror Hultberg

#    This file is part of CG_module.

#    CG_module is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    CG_module is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


class List:
    def __init__(self, setname, taglist):
        self.setname = setname
        self.taglist = taglist

    def __str__(self):
        return('LIST ' + self.setname + ' = ' + self.taglist + ' ;')


class Set:
    def __init__(self, setname, inlineset):
        self.setname = setname
        self.inlineset = inlineset

    def __str__(self):
        return('SET ' + self.setname + ' = ' + self.inlineset + ' ;')


class Select:
    def __init__(self, target, match):
        self.target = target
        self.match = match

    def __str__(self):
        return("SELECT " + self.target + " IF " + self.match + ' ;')


class Remove:
    def __init__(self, target, match):
        self.target = target
        self.match = match

    def __str__(self):
        return("REMOVE " + self.target + " IF " + self.match + ' ;')


class Rule(Select, Remove):
    pass


class CG:

    def __init__(self, delimiters, soft_delimiters, rules, sets):
        self.delimiters = delimiters
        self.soft_delimiters = soft_delimiters
        self.rules = rules
        self.sets = sets

    def __str__(self):
        finalcg = self.delimiters + "\n" + self.soft_delimiters + "\n" + 'SETS'
        for set in self.sets:
            finalcg = finalcg + str(set) + "\n"
        finalcg = finalcg + 'SECTION'
        for rule in self.rules:
            finalcg = finalcg + str(rule) + "\n"
        return(finalcg)


set1 = List(setname="Pr", taglist="(pr)")
set2 = List(setname="Adj", taglist="(adj)")
set3 = Set(setname="N", inlineset="(1 VERB)")

rule1 = Select(target="N", match="(1 VERB)")
rule2 = Select(target="N", match="(-1 ADJ)")
rule3 = Remove(target="N", match="(1 VERB)")


rules = [rule1, rule2, rule3]
sets = [set1, set2, set3]
cg = CG

delimiters = 'DELIMITERS = "<.>" "<!>" "<?>" "<...>" "<¶>" "<:>" ;'
soft_delimiters = 'SOFT-DELIMITERS = "<,>" ;'

cg = CG(delimiters, soft_delimiters, rules, sets)
print(cg)


