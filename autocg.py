#!/usr/bin/python3
#
# Copyright (C) 2016 Bror Hultberg
# Copyright (C) 2016 Joonas Kylmälä
#
# This file is part of autocg.
#
# autocg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# autocg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autocg.  If not, see <http://www.gnu.org/licenses/>.


import cg
import parser
import argparse
from streamparser import parse_file


def make_cg_list(tag):
    cg_list = cg.List(setname=tag.upper(), taglist=[tag])
    return cg_list


def parse_args():
    parser = argparse.ArgumentParser(description='Generate CG rules')
    parser.add_argument('corpus')
    parser.add_argument('-t', '--threshold',
                        default=0.08,
                        type=float,
                        help='threshold value')
    parser.add_argument('-m', '--min-count',
                        default=100,
                        type=int,
                        help='taking account only features with at least this frequency count')
    return parser.parse_args()

def main():
    args = parse_args()
    corpus = parser.wordclass(parser.remove_useless(parse_file(open(args.corpus))))
    unigrams = parser.ngram_count(corpus, 1)
    bigrams = parser.ngram_count(corpus, 2)
    probabilities = parser.comb_probabilities(corpus, unigrams, bigrams)
    local_context_rules = parser.local_context_rules(probabilities,
                                                     unigrams,
                                                     args.min_count,
                                                     args.threshold)
    tags = parser.get_tags(corpus)
    sets = [make_cg_list(tag) for tag in tags]
    delimiters = 'DELIMITERS = "<.>" "<!>" "<?>" "<...>" "<¶>" "<:>" ;'
    soft_delimiters = 'SOFT-DELIMITERS = "<,>" ;'
    cg_file = cg.CG(delimiters, soft_delimiters, local_context_rules, sets)
    print(cg_file)


if __name__ == '__main__':
    main()
