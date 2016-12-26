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


import cg
import parser
from streamparser import parse_file


def main():
    x = input()
    corpus = parser.wordclass(parser.remove_useless(parse_file(open(x))))
    unigrams = parser.ngram_count(corpus, 1)
    bigrams = parser.ngram_count(corpus, 2)
    probabilities = parser.comb_probabilities(corpus, unigrams, bigrams)
    local_context_rules = parser.local_context_rules(probabilities)
    sets = []
    delimiters = 'DELIMITERS = "<.>" "<!>" "<?>" "<...>" "<¶>" "<:>" ;'
    soft_delimiters = 'SOFT-DELIMITERS = "<,>" ;'
    cg_file = cg.CG(delimiters, soft_delimiters, local_context_rules, sets)
    print(cg_file)

if __name__ == '__main__':
    main()
