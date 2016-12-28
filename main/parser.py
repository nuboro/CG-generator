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

import math
import cg
import collections
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
    for feat_position, first_feature in enumerate(sequence):
        if first_feature == start:
            candidate_features = set()
            for later_feature in sequence[feat_position + 1:]:
                if later_feature != end:
                    candidate_features.add(later_feature)
                else:
                    features.add(frozenset(candidate_features))
                    break
    return(features)


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


def ngram_count(items, n):
    features = []
    for j in range(len(items)-n+1):
        possible_contexts = items[j:j+n]
        features = features + combine(possible_contexts)
    features = tuple(tuple(feature) for feature in features)
    feature_count = {feature: 0 for feature in features}
    for feature in features:
        feature_count[feature] = feature_count[feature] + 1
    return(feature_count)


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
        useless = False
        for reading in cohort.readings:
            for subreading in reading:
                if is_useless(subreading):
                    useless = True
        if not useless:
            yield cohort


def is_useless(subreading):
    useless_tags = ['sent', 'cm', 'lquot', 'rquot', 'lpar', 'rpar',
                    'guio', 'lquest']
    for tag in subreading.tags:
        if tag in useless_tags:
            return True
    return False


def moivre_laplace_probability(corpus, bigram, f, N):
    P = f + 1.96 * math.sqrt(f*(1-f)/N)
    return(P)


def upper_limit_zero_relative(N):
    P = 1-0.025**(1/N)
    return(P)


def frequency_count(unigrams, feature):
    N = unigrams[(feature,)]
    return(N)


def relative_frequence(bigrams, unigrams, bigram, feature):
    f = bigrams[bigram]/unigrams[(feature,)]
    return(f)


def probability(bigrams, unigrams, corpus, bigram, position):

    P_of_bigram = {}
    feat_in_con = collections.namedtuple('feat_in_con', 'bigram feature')
    feature = bigram[position]
    P = get_upper_limit(bigrams, unigrams, corpus, feature, bigram)
    P_of_bigram[feat_in_con(bigram, position)] = P
    return(P_of_bigram)


def get_upper_limit(bigrams, unigrams, corpus, feature, bigram):
    context = bigram[(bigram.index(feature) + 1) % 2]
    N = frequency_count(unigrams, feature)
    if bigram in bigrams:
        f = relative_frequence(bigrams, unigrams, bigram, feature)
        P = (moivre_laplace_probability(corpus, bigram, f, N))
    else:
        P = (upper_limit_zero_relative(N))
    return(P)


def prob_1C(corpus, bigram, unigrams, bigrams):
    probability_P = probability(bigrams, unigrams, corpus, bigram, 0)
    return(probability_P)


def prob_negative_1C(corpus, bigram, unigrams, bigrams):
    probability_P = probability(bigrams, unigrams, corpus, bigram, 1)
    return(probability_P)


def comb_probabilities(corpus, unigrams, bigrams):
    probabilities = []
    for seq in pos_bigrams(get_tags(corpus)):
        bigram = tuple(seq)
        probabilities.append(prob_1C(corpus, bigram, unigrams, bigrams))
        probabilities.append(prob_negative_1C(corpus, bigram, unigrams, bigrams))
    return(probabilities)


def local_context_rules(probabilities, unigrams, y, threshold):
    local_context_rules = []
    for probability in probabilities:
        if (list(probability.values())[0]) < threshold:
            bigram = (list(probability.keys())[0].bigram)
            position_feature = list(probability.keys())[0].feature
            feature = bigram[position_feature]
            context = bigram[(position_feature+1) % 2]
            if frequency_count(unigrams, feature) >= int(y) and frequency_count(unigrams, context) >= int(y):
                if position_feature == 0:
                    rule = cg.Remove(target=feature.upper(), match="(1C " + context.upper() + ")")
                    local_context_rules.append(rule)
                elif position_feature == 1:
                    rule = cg.Remove(target=feature.upper(), match="(-1C " + context.upper() + ")")
                    local_context_rules.append(rule)
    return(local_context_rules)


def get_tags(corpus):
    tags = set()
    for features in corpus:
        for feature in features:
            tags.add(feature)
    return(list(tags))


def pos_bigrams(tags):
    bigrams = []
    for tag in tags:
        for tag2 in tags:
            bigrams.append([tag, tag2])
    return(bigrams)


def main():
    cohorts = parse_file(fileinput.input())
    cohorts = remove_useless(cohorts)
    probabilities = prob(wordclass(cohorts))
    print(probabilities)


if __name__ == '__main__':
    main()
