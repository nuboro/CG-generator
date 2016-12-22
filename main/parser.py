# Copyright (C) 2016 Bror Hultberg
# Copyright (C) 2016 Joonas Kylmälä
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

import fileinput
from streamparser import parse_file


def combine(a):
    if len(a) == 1:
        return([[x] for x in a[0]])
    else:
        return([[x]+y for x in a[0] for y in combine(a[1:])])


def features_between(sequence, start, end):
    """Return from sequence features that are between the start and end tag"""
    features = set()
    for j in range(len(sequence)):
        barrier = set()
        if sequence[j] == start:
            try:
                for i in range(len(sequence)-j+1):
                    if sequence[i+j+1] != end:
                        barrier.add(sequence[i+j+1])
                    else:
                        froz_barrier = frozenset(barrier)
                        features.add(froz_barrier)
                        break
            except IndexError:
                barrier.clear()
    return(features)


def pos(my_list, element):
    indices = [i for i, x in enumerate(my_list) if x == element]
    return(indices)


def barrier(x, start, end):
    """returns a set of set of features(barrier) from given cohorts (x) that occur between string:"start" and string:"end"
    """
    list_of_features = combine(wordclass(x))
    final_barrier = set()
    for sequence in list_of_features:
        froz_barrier = features_between(sequence, start, end)
        final_barrier = final_barrier | froz_barrier
    return(final_barrier)


def prob(items):
    features = []
    for item in items:
        for feature in item:
            features.append(feature) 
    feature_pos = {x: features.count(x)/len(items) for x in features}

    return(feature_pos)


def wordclass(cohorts):
    return(get_features(cohorts, lambda x: x.tags[0]))


def baseform(cohorts):
    return(get_features(cohorts, lambda x: x.baseform))


def get_features(cohorts, feature):
    features = []
    for cohort in cohorts:
        posfeatures = set()
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
    useless_tags = ['sent', 'cm', 'lquot', 'rquot', 'lpar', 'rpar', 'guio']
    for tag in subreading.tags:
        print(subreading)
        if tag in useless_tags:
            return True
    return False


def main():
    cohorts = parse_file(fileinput.input())
    cohorts = remove_useless(cohorts)
    probabilities = prob(wordclass(cohorts))

    print(probabilities)


main()
# x=input()
# y=input()
# z=input()
# print(wordclass(prepros(x)))
# print(combine(wordclass(prepros(x))))
# print(barrier(x,y,z))
