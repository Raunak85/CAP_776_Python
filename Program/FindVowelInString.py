strg = """BERT, or Bidirectional Encoder Representations from Transformers, is a machine learning (ML) framework for natural language processing 
(NLP) that Google introduced in 2018. BERT uses a transformer encoder architecture to learn to represent text as a sequence of vectors by 
considering the context of words in both forward and backward directions. The goal is to help computers understand the meaning of ambiguous 
language in text by using surrounding text to establish context. BERT is trained on large amounts of language data, including English Wikipedia 
and the Brown Corpus, and continues to learn through unsupervised learning from unlabeled text."""

temp = strg.lower()
count = 0
for i in temp:
    if(i == 'a' or i == 'e' or i == 'o' or i == 'i' or i == 'u'):
        count += 1
print(count)

