from operator import index
import tqdm
from gensim.models import CoherenceModel
from pprint import pprint
import gensim.corpora as corpora
import spacy
from nltk.corpus import stopwords
from gensim import corpora, models
import errno
import socket
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import re
import shutil
import random

if __name__ == '__main__':
    # Step 1: Import data

    # nltk.download('wordnet')
    # nltk.download('omw-1.4')

    df = pd.read_csv(
        'C:/path/Full_Meta.csv')

    # Step 2: Data preprocessing

    # keep only text
    data_text = df[['Titles']]
    documents = data_text
    print(len(documents))

    # remove punctuation
    documents['Titles_preprocessed'] = documents['Titles'].map(
        lambda x: re.sub('[,\!?.]', '', x))
    documents['Titles_preprocessed'] = documents['Titles'].map(
        lambda x: x.lower())

    # Tokenize titles

    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    data = documents.Titles_preprocessed.values.tolist()
    data_words = list(sent_to_words(data))

    print(data_words[:1][0][:30], '======RAW==========')

    # Build the bigram and trigram models
    # min count = pair appears min x times count, threshold = pair count exceeds threshold
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # NLTK Stop words, !! remeber to download on first run !!
    # nltk.download('stopwords')

    stop_words = stopwords.words('english')
    stop_words_extra = [
        'india',
        'china',
        "jnj",
        "roche",
        "Pfizer",
        "AbbVieGlobal",
        "novonordisk",
        "novartis",
        "elilillyandco",
        "BristolMyersSquibb",
        "CVSHealth",
        "GSK",
        "amgenbiotech",
        "Regeneron",
        "modernatx",
        "Bayer",
        "LonzaGroupAG",
        "Biogen",
        "SunPharmaLive",
        "HorizonTherapeutics",
        "PPDCRO",
        "Servier",
        "boehringeringelheim",
        "Abbott",
        "Incyte",
        "Dr.ReddysLaboratoriesLtd",
        'janssen',
        'sunpharma',
        'bayer',
        'https',
        'lilli',
        'lilly',
        'gsk',
        'abbo_tt',
        'wearelilli',
        'wearelilly',
        'johnson_johnson',
        'jnj',
        'ppd',
        'johnson',
        'pfizer',
        'moderna',
        'ppdcareer',
        'amgen',
        'bit',
        'http_ow',
        'drreddys',
        'dr_reddy',
        'see',
        'ly',
        'www',
        'datum',
        'http',
        'com',
        'dr_abbot']

    # Define functions for stopwords, bigrams, trigrams and lemmatization

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    def remove_stopwords_extra(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words_extra] for doc in texts]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams_raw = make_bigrams(data_words_nostops)

    # Remove redundant words
    data_words_bigrams = remove_stopwords_extra(data_words_bigrams_raw)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[
                                    'NOUN', 'ADJ', 'VERB', 'ADV'])

    print(data_lemmatized[:1])

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)
    # Fix dic for comparable results
    id2word.save("filename")

if __name__ == '__main__':
    # Load after passing once
    id2word = corpora.Dictionary.load("filename")
    # id2word.filter_extremes under 13 frequency
    id2word.filter_extremes(no_below=14, no_above=1)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    print(corpus[:1][0][:30], 'CORPUUUUUUUSSSS')

    # Build LDA model
    lda_model = gensim.models.LdaMulticore(
        corpus=corpus, id2word=id2word, num_topics=5, random_state=1, chunksize=100, passes=10, alpha='symmetric', eta=0.61)

    # Print the Keyword in the k topics
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(
        model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print(coherence_lda)
    while coherence_lda < 0.43:
        lda_model = gensim.models.LdaMulticore(
            corpus=corpus, id2word=id2word, num_topics=5, random_state=1, chunksize=100, passes=10, alpha='symmetric', eta=0.61)

        doc_lda = lda_model[corpus]
        # Compute Coherence Score
        coherence_model_lda = CoherenceModel(
            model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print(coherence_lda)

    import pickle
    import pyLDAvis
    import pyLDAvis.gensim_models as gensimvis
    # Visualize the topics

    visualisation = gensimvis.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(visualisation, 'LDA_Visualization.html')

    pprint(lda_model.print_topics())
    result = []
    for i in range(len(documents)):
        values = []
        for i in lda_model[corpus[i]]:
            count = 0
            for j in i:
                count += 1
                if count % 2 == 0:

                    values.append(j)
        result.append(values)

    results = pd.DataFrame(result)
    results.to_csv('LDA_RESULTS.csv')

    print('\nCoherence Score: ', coherence_lda)
    print('corpus 0 ------------------------------------------',
          lda_model[corpus[0]])
    allocation = []
    for i in range(corpus):
        allocation.append(corpus[i])

    # supporting function

    def compute_coherence_values(corpus, dictionary, k, a, b):

        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=dictionary,
                                               num_topics=k,
                                               random_state=1,
                                               chunksize=100,
                                               passes=10,
                                               alpha=a,
                                               eta=b)
        coherence_model_lda_train = CoherenceModel(
            model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')

        return coherence_model_lda_train.get_coherence()

    grid = {}
    grid['Validation_Set'] = {}
    # Topics range
    min_topics = 2
    max_topics = 12
    step_size = 1
    topics_range = range(min_topics, max_topics, step_size)
import numpy as np
# Alpha parameter
alpha = list(np.arange(0.01, 1, 0.3))
alpha.append('symmetric')
alpha.append('asymmetric')
print(alpha)
# Beta parameter
beta = list(np.arange(0.01, 1, 0.3))
beta.append('symmetric')
# Validation sets
print(len(corpus), 'lencorpppppppuuuuuuussss')
num_of_docs = len(corpus)
print('dis is da next part ma g')
corpus_sets = [  # gensim.utils.ClippedCorpus(corpus, num_of_docs*0.25),
    # gensim.utils.ClippedCorpus(corpus, num_of_docs*0.5),
    gensim.utils.ClippedCorpus(corpus, int(num_of_docs*0.75)),
    corpus]
corpus_title = ['75% Corpus', '100% Corpus']
model_results = {'Validation_Set': [],
                  'Topics': [],
                   'Alpha': [],
                  'Beta': [],
                     'Coherence': []
                  }
 # Can take a long time to run
 if 1 == 1:
      pbar = tqdm.tqdm(total=540)

       # iterate through validation corpuses
       for i in range(len(corpus_sets)):
            # iterate through number of topics
            for k in topics_range:
                # iterate through alpha values
                for a in alpha:
                    # iterare through beta values
                    for b in beta:
                        # get the coherence score for the given parameters
                        cv = compute_coherence_values(corpus=corpus_sets[i], dictionary=id2word,
                                                      k=k, a=a, b=b)
                        # Save the model results
                        model_results['Validation_Set'].append(corpus_title[i])
                        model_results['Topics'].append(k)
                        model_results['Alpha'].append(a)
                        model_results['Beta'].append(b)
                        model_results['Coherence'].append(cv)

                        pbar.update(1)
        pd.DataFrame(model_results).to_csv(
            'lda_tuning_results.csv', index=False)
        pbar.close()
