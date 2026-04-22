
import numpy 
from sentence_transformers import SentenceTransformer
import httpx
import os
import gzip
import csv
from pathlib import Path





############################################################################################################################################################################################################################################
#Prepare and see GFF file#
############################################################################################################################################################################################################################################

URL_gff = "https://north-1.cloud.snic.se:8080/swift/v1/AUTH_d9d5ac98cb2b4a3091b60040077e8efc/plantgenie-knowledge/Picab02_230926_at01_all_sorted.gff3.gz"

pgff = Path(__file__).resolve().parent / "Picab02_230926_at01_all_sorted.gff3"

if not pgff.exists():
    response = httpx.get(URL_gff, follow_redirects=True)
    content = gzip.decompress(response.content)
    pgff.write_bytes(content)
# text = pgff.read_text()


# lines = text.splitlines()
# print(f"Total lines in file: {len(lines)}")
# print("\nFirst 10 lines:")
# for line in lines[:10]:
#     print(line)



############################################################################################################################################################################################################################################
#Turn {ID: description} into a csv file#
############################################################################################################################################################################################################################################



URL_tsv= "https://north-1.cloud.snic.se:8080/swift/v1/AUTH_d9d5ac98cb2b4a3091b60040077e8efc/plantgenie-knowledge/Picab02_230926_at01_longest_representative_annotations_merged_sorted_non_redundant_panthers.tsv.gz"
p = Path(__file__).resolve().parent / "Picab02_230926_at01_longest_representative_annotations_merged_sorted_non_redundant_panthers.tsv"


if not p.exists():
    response = httpx.get(URL_tsv, follow_redirects=True)
    content = gzip.decompress(response.content)
    p.write_bytes(content)
text = p.read_text()
lines = text.splitlines()




with open('annotations.csv', 'w', newline='') as t:
    writer = csv.writer(t)
    writer.writerow([ "ID", "Eggnog_description" ])
    for line in lines: 
        columns = line.split("\t")
        writer.writerow([
            columns[0],
            columns[4]
        ])

print("\n\n\nDone writing annotations.csv\n\n\n")





############################################################################################################################################################################################################################################
#Turn embeddings.npy into a csv file#
############################################################################################################################################################################################################################################


model = SentenceTransformer(
    "mixedbread-ai/mxbai-embed-large-v1",
    prompts={"retrieval": "Represent this sentence for searching relevant passages: "},
)


ID = []
description = []

for line in lines:
    columns = line.split("\t")
    ID.append(columns[0])
    description.append(columns[4])



gene_ids_file = "gene-ids.npy"
embeddings_file = "annotations-embeddings.npy"

if os.path.exists(embeddings_file):
    # print("Loading embeddings from disk...")
    embeddings = numpy.load(embeddings_file)
    gene_ids = list(numpy.load(gene_ids_file, allow_pickle=True))
else:
    print(f"Computing embeddings for {len(description)} gene descriptions...")
    embeddings = model.encode(description, show_progress_bar=True)
    numpy.save(embeddings_file, embeddings)
    numpy.save(gene_ids_file, numpy.array(ID, dtype=object))
    print("\n\nEmbeddings saved to disk.")
    print(f"\n\nEmbedding matrix shape: {embeddings.shape}")



with open('embeddings.csv', 'w', newline='') as e:
    writer = csv.writer(e)
    writer.writerow(['gene_id'] + [f'dim_{i}' for i in range(embeddings.shape[1])])
    for gene_id, vec in zip(gene_ids, embeddings):
        writer.writerow([gene_id] + vec.tolist())

print('\n\n\nDone writing embeddings.csv')
