Create view small_bed as 
SELECT ID, Eggnog_description, Embeddings 
from genes_bedded
where Feature = 'gene';
--78.4k rows

Create table clean_small_bed as 
Select * from small_bed
where Eggnog_description is not null; 
--32,225 rows

Create table Cosine_similarity AS
SELECT x.ID AS ID_1, 
y.ID AS ID_2,
array_cosine_similarity(
x.embeddings, y.embeddings
) AS similarity_metric
FROM clean_small_bed AS x
CROSS JOIN clean_small_bed AS y
WHERE ID_1 > ID_2
ORDER BY similarity_metric DESC; 