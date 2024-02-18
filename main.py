from ranking import Ranking
import json

def main():
   with open("documents.json", 'r', encoding="utf-8") as file:
      documents = json.load(file)

   # Defining the index files and the associated coefficients
   index_files = {"content_pos_index.json": 1, "title_pos_index.json": 3}

   # Instanciating the ranker
   ranking = Ranking(index_files=index_files)

   # Searching
   while True:
      query = input("Enter a query: ")
      results = ranking.search(query, index_files=index_files, type="OR")
      results_id = [int(result[0]) for result in results]
      for r in results_id:
         print(f"Doc n°{r} - {documents[r]['url']} - {documents[r]['title'][:50]}")

if __name__ == "__main__":
   main()