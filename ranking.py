import spacy
import json
import math


class Ranking:
   def __init__(self, index_files):
      """Initializes the ranker."""
      model = "fr_core_news_md"
      self.nlp = spacy.load(model)

      # Loading the indexes
      self.indexes = []
      for index_file in index_files:
         with open(index_file, 'r', encoding="utf-8") as file:
            index = json.load(file)
         n_docs = len(index)
         avg_tokens_per_doc = sum([len(doc) for doc in index.values()]) / n_docs
         self.indexes.append({
            "index": index,
            "coef": index_files[index_file],
            "n_docs": n_docs,
            "avg_tokens_per_doc": avg_tokens_per_doc,
            "dl": self.compute_dl(index)})
   
   def compute_dl(self, index):
      """Computes the length of the documents in the index."""
      dl = {}
      for token in index:
         for doc_id in index[token]:
            if not doc_id in dl:
               dl[doc_id] = 0
            dl[doc_id] += len(index[token][doc_id])
      return dl

   def search(self, query, index_files, type = "AND"):
      """Searches for documents matching the query."""
      # Lemmatizing
      query_tokens = self.lemmatize([query])[0]

      # Searching
      if type == "AND":
         results = self.search_and(query_tokens)
      else:
         results = self.search_or(query_tokens)   
      return results   
   
   def search_and(self, query_tokens):
      """Searches for documents matching the query with the AND operator."""
      scores = {}
      for index in self.indexes:
         index_scores = self.bm25(query_tokens, index["index"], index["n_docs"], index["avg_tokens_per_doc"], index["dl"])
         for doc_id, score in index_scores.items():
               if doc_id in scores:
                  scores[doc_id] += score * index["coef"]
               else:
                  scores[doc_id] = score * index["coef"]

      # Filter out documents that don't have scores for all query terms
      relevant_docs = {}
      for doc_id, _ in scores.items():
         if all(token in index["index"] for token in query_tokens):
               relevant_docs[doc_id] = scores[doc_id]

      sorted_results = sorted(relevant_docs.items(), key=lambda x: x[1], reverse=True)
      return sorted_results[:10]


   def search_or(self, query_tokens):
      """Searches for documents matching the query with the OR operator."""
      scores = {}
      for index in self.indexes:
         index_scores = self.bm25(query_tokens, index["index"], index["n_docs"], index["avg_tokens_per_doc"], index["dl"])
         for doc_id, score in index_scores.items():
            if doc_id in scores:
               scores[doc_id] += score * index["coef"]
            else:
               scores[doc_id] = score * index["coef"]
      sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
      return sorted_results[:10]

   def bm25(self, query_tokens, index, N, avgdl, dl_dict, k1=1.5, b=0.75):
      """Computes the BM25 score of the documents in the index."""
      scores = {}
      for token in query_tokens:
         if token in index:
            n = len(index[token])
            idf = math.log((N - n + 0.5) / (n + 0.5))
            for doc_id, f_ in index[token].items():
               f = f_["count"]
               dl = dl_dict[doc_id]
               tf = f / dl
               score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
               if doc_id in scores:
                  scores[doc_id] += score
               else:
                  scores[doc_id] = score
      return scores

   def lemmatize(self, docs):
      """Lemmatizes a list of documents."""
      docs = list(self.nlp.pipe(docs, disable=["parser", "ner"]))
      new_docs = []
      for i, doc in enumerate(docs):
         new_docs.append([])
         for token in doc:
            if token.is_alpha and not token.is_stop:
               new_docs[i].append(token.lemma_.lower())
      return new_docs

if __name__ == '__main__':
   index_files = {"content_pos_index.json": 1, "title_pos_index.json": 3}
   ranking = Ranking(index_files=index_files)
   while True:
      query = input("Enter a query: ")
      print(ranking.search(query, index_files=index_files, type="OR"))