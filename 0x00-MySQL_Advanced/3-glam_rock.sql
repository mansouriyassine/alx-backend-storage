-- List bands with Glam rock as main style, ranked by longevity

-- Calculate the lifespan for each band
SELECT band_name, 
       IF(splitted[2] IS NOT NULL, 
          2022 - CAST(splitted[2] AS UNSIGNED), 
          2022 - CAST(splitted[1] AS UNSIGNED)) AS lifespan
FROM (
    -- Extract the start and end years from the formed attribute
    SELECT band_name, 
           SPLIT_STR(formed, '-', 1) AS formed_year,
           SPLIT_STR(formed, '-', 2) AS disbanded_year
    FROM metal_bands
    WHERE style LIKE '%Glam rock%'
) AS subquery
ORDER BY lifespan DESC;