# SECOS - SEmantic COmpound Splitter

SECOS is an unsupervised compound splitter. Details about its working can be found in:

Martin Riedl, Chris Biemann (2016): Unsupervised Compound Splitting With Distributional Semantics Rivals Supervised Methods, In: Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2016), San Diego, CA, USA

## Split compounds


python decompound_secos.py dt_candidates word_count_file min_word_count(50) file_compound word_index prefix_length(3) suffix_length(3) word_length(5) dash_word(3) upper(upper) epsilon
-----------------------------------------------------
Parameter description:
-----------------------------------------------------
dt_candidates:		file with words and their split candidates, generated from a distributional thesaurus (DT)
word_count_file:	file with word counts used for filtering
min_word_count:		minimal word count used for split candidates (recommended paramater: 50)
file_compound:		file with words that should be decompounded (each compound needs to be in a single line)
word_index:		index of the word in the tab separated file_compound
prefix_length:		length of prefixes that are appended to the right-sided word (recommended parameter: 3)
suffix_length:		length of suffixes that are appended to the left-sided word (recommended parameter: 3)
word_length:		minimal word length that is used from the split candidates (recommended parameter: 5)
dash_word:		heuristic to split words with dash, which has no big impact (recommended: 3)
upper:			consider uppercase letters (=upper) or not (=lower). Should be set for case-sensitive languages e.g. German
epsilon:		smoothing factor (recommended parameter: 0.01


### Example for German
python decompound_secos.py data/denews70M_tokenized_trigram__candidates data/denews70M_tokeniyed_trigram__WordCount 50 german_compounds 0 3 3 5 3 upper 0.01


### Example for Dutch
python decompound_secos.py data/dutch_cow_trigram__candidates data/dutch_cow_trigram__WordCount 50 dutch_compounds 0 3 3 5 3 lower 0.01


## Training new language

cat dt | python generateDecompoundCandidates.py > dt_candidates

The DT is a file of 3 tab separated columns with two words and their similarity score. The file needs to be ordered by the first word and the similarity score in descending ordering. The DT is generated using JoBimText (www.jobimtext.org) using only neighboring words by using the Trigram holing operation.


## Evaluation

will follow soon

## Comparing results with significance test

will follow as well
