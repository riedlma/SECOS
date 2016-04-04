# SECOS - SEmantic COmpound Splitter

SECOS is an unsupervised compound splitter that uses information from a distributional thesaurus (DT). Details about its working can be found in our [paper](https://www.lt.informatik.tu-darmstadt.de/de/publications/details/?no_cache=1&tx_bibtex_pi1[pub_id]=TUD-CS-2016-0071).


## Split compounds

In order to split compounds SECOS features some parameters and requires a candidate file, which is generated using a distributional thesaurus. In order to use SECOS for splitting German and Dutch compounds, you can use pre-computed candidate lists and the commands shown below.

```
python decompound_secos.py dt_candidates word_count_file min_word_count(50) file_compound word_index prefix_length(3) suffix_length(3) word_length(5) dash_word(3) upper(upper) epsilon
-----------------------------------------------------
Parameter description:
-----------------------------------------------------
dt_candidates:		file with words and their split candidates, generated from a distributional thesaurus (DT)
word_count_file:	file with word counts used for filtering
min_word_count:		minimal word count used for split candidates (recommended paramater: 50)
file_compound:		file with words that should be decompounded (each compound needs to be in a single line)
word_index:			index of the word in the tab separated file_compound
prefix_length:		length of prefixes that are appended to the right-sided word (recommended parameter: 3)
suffix_length:		length of suffixes that are appended to the left-sided word (recommended parameter: 3)
word_length:		minimal word length that is used from the split candidates (recommended parameter: 5)
dash_word:			heuristic to split words with dash, which has no big impact (recommended: 3)
upper:				consider uppercase letters (=upper) or not (=lower). Should be set for case-sensitive languages e.g. German
epsilon:			smoothing factor (recommended parameter: 0.01
```

### Apply SECOS to German Compounds

In order to compound German words you need to download and unzip the following package: [data.zip](https://maggie.lt.informatik.tu-darmstadt.de/files/SECOS/data.zip). Using these files, a list of compounds (german_compounds) can be split using the following command:


```
python decompound_secos.py data/denews70M_tokenized_trigram__candidates data/denews70M_tokeniyed_trigram__WordCount 50 german_compounds 0 3 3 5 3 upper 0.01
```


### Apply SECOS to Dutch Compounds
In order to compound Dutch words you need to download and unzip the following package: [data.zip](https://maggie.lt.informatik.tu-darmstadt.de/files/SECOS/data.zip). Using these files, a list of compounds (dutch_compounds) can be split using the following command:

```
python decompound_secos.py data/dutch_cow_trigram__candidates data/dutch_cow_trigram__WordCount 50 dutch_compounds 0 3 3 5 3 lower 0.01
```


## Training Candidates for New Language
In order to train candidates for a new language, a distributional thesaurus (DT) is required. The DT is a file of 3 tab separated columns with two words and their similarity score. The file needs to be ordered by the first word and the similarity score in descending ordering. The DT is generated using JoBimText (www.jobimtext.org) using only neighboring words by using the Trigram holing operation.
Using such a DT the candidates can easily be generated with the following command:

```
cat dt | python generateDecompoundCandidates.py > dt_candidates
```



## Evaluation


For the evaluation the python script eval_decompounding.py can be used. It expects as stdin a tab separated file including the gold standard and the predicted splits which are separated with dashs (-).

Here an example for a compound file (compound_file) where column 1 contains the predicted splits and column 2 the gold standard split

```
cat compound_file | python eval_decompounding.py 1 2 
```

This command results to the following output (precision, recall and F1 measure based on the splits (the third row rounds to 4 digits). The last column presents the number of compounds considered and the amount of entirely correctly split compounds as well as the rate of correct split compounds.

```
Precision       Recall       F1
0.986667        0.964335     0.975373
0.9867 &        0.9643&      0.9754
Considered      Correct      Percentage of Correct ones
700.000000      662.000000   0.945714

```

A detailed output of correct and false splits can be enabled by providing a third parameter:

```
cat compound_file | python eval_decompounding.py 1 2 debug
```


## Comparing results with significance test

In addition to the above evaluation script, we also provide an evaluation script that can be used to compute a significance test between two methods. For this we use a Wilcoxon rank sum test and compare the performance based on the F1 score of each split compound. The test can be started using the following command:

```
python eval_decompounding_wilcoxon.py compound_file_1 predicted_compound gold_compound compound_file_2 predicted_compound gold_compound
```



# Citation:

If you use SECOS, please cite the following work:

```
@inproceedings{riedl2016secos,
    title={Unsupervised Compound Splitting With Distributional Semantics Rivals Supervised Methods },
    author={Martin Riedl, Chris Biemann},
    booktitle={Proceedings of The 15th Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologie},
    pages={},
    year={2016},
    address={San Diego, CA, USA},
}
```

# License:

Apache License (ASL) 2.0
