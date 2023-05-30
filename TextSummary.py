import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import PyPDF2

def convert(file):
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)

    text = ""
    for page in range(num_pages):
        text += reader.pages[page].extract_text()
    return text

def summarize(text):
    # list of stop words
    stopwords = list(STOP_WORDS)

    # list of other words that are not in stopwords or punctuation
    list1 = ["\n"]

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # storing each word in dictionary
    tokens = [token.text for token in doc]

    # frequency of each word except punctuation and stop words
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation and word.text.lower() not in list1:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    # print(word_freq)

    # maximum frequency
    max_freq = max(word_freq.values())

    # normalized frequency
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    # sentence dictionary
    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    #print(summary)
    return summary