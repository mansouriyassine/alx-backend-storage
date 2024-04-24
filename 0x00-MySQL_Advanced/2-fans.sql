-- Rank country origins of bands by the number of fans

-- Calculate the number of fans for each country origin
SELECT origin, COUNT(*) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;