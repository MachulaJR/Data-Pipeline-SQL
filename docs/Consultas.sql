-- Top 5 carros com maior torque por marca:
SELECT "Marca", "Modelo", "Torque"
FROM (
	SELECT "Marca", "Modelo", "Torque",
		ROW_NUMBER() OVER (PARTITION BY "Marca" ORDER BY "Torque" DESC, "Modelo") AS RN
	FROM cars_db_tratado
) RANKED
WHERE RN = 1
ORDER BY "Torque" DESC
LIMIT 5;

-- Top 5 carros com mais cavalos de potencia por marca:
SELECT "Marca", "Modelo", "Potencia"
FROM (
	SELECT "Marca", "Modelo", "Potencia",
		ROW_NUMBER() OVER (PARTITION BY "Marca" ORDER BY "Potencia" DESC, "Modelo") AS RN
	FROM cars_db_tratado
) RANKED
WHERE RN = 1
ORDER BY "Potencia" DESC
LIMIT 5;

-- Top 5 carros com maior velocidade maxima:
SELECT "Marca", "Modelo", "Velocidade_Maxima"
FROM (
	SELECT "Marca", "Modelo", "Velocidade_Maxima",
		ROW_NUMBER() OVER (PARTITION BY "Marca" ORDER BY "Velocidade_Maxima" DESC, "Modelo") AS RN
	FROM cars_db_tratado
) RANKED
WHERE RN = 1
ORDER BY "Velocidade_Maxima" DESC
LIMIT 5;

-- Top 5 carros com menor aceleracao 0 a 100 Km/h por marca:
SELECT "Marca", "Modelo", "Aceleracao_0_100"
FROM (
	SELECT "Marca", "Modelo", "Aceleracao_0_100",
		ROW_NUMBER() OVER (PARTITION BY "Marca" ORDER BY "Aceleracao_0_100" DESC, "Modelo") AS RN
	FROM cars_db_tratado
) RANKED
WHERE RN = 1
ORDER BY "Aceleracao_0_100" aSC
LIMIT 5;

-- Top 5 carros mais caros por marca:
SELECT "Marca", "Modelo", "Preco"
FROM (
	SELECT "Marca", "Modelo", "Preco",
		ROW_NUMBER() OVER (PARTITION BY "Marca" ORDER BY "Preco" DESC, "Modelo") AS RN
	FROM cars_db_tratado
) RANKED
WHERE RN = 1
ORDER BY "Preco" DESC
LIMIT 5;

--Top 5 marcas com maior quantidade de modelos de carros:
SELECT "Marca", COUNT(*) AS Quantidade_Modelos
FROM cars_db_tratado
GROUP BY "Marca"
ORDER BY Quantidade_Modelos DESC
LIMIT 5;

--Top 5 motores com maior quantidade de modelos:
SELECT "Motor", COUNT(*) AS Quantidade_Motores
FROM cars_db_tratado
GROUP BY "Motor"
ORDER BY Quantidade_Motores DESC
LIMIT 5;

--Analise Preço x Velocidade Maxima Media:
SELECT 
	(SELECT ROUND(AVG("Velocidade_Maxima"), 2) 
	FROM cars_db_tratado
	WHERE "Preco" <= 500000) AS Até_500k, 
	
	(SELECT ROUND(AVG("Velocidade_Maxima"), 2) 
	FROM cars_db_tratado
	WHERE "Preco" BETWEEN 500000 AND 1000000) AS De_500k_até_1M,
	
	(SELECT ROUND(AVG("Velocidade_Maxima"), 2) 
	FROM cars_db_tratado
	WHERE "Preco" BETWEEN 1000000 AND 10000000) AS De_1M_até_10M,
	
	(SELECT ROUND(AVG("Velocidade_Maxima"), 2) 
	FROM cars_db_tratado
	WHERE "Preco" > 10000000) AS Acima_10M;
	
--Analise Motores x Velocidade Maxima Media:
SELECT 
	(SELECT ROUND(AVG("Velocidade_Maxima"), 2)
	FROM cars_db_tratado
	WHERE "Motor" LIKE '%V6%') AS Motor_V6,

	(SELECT ROUND(AVG("Velocidade_Maxima"), 2)
	FROM cars_db_tratado
	WHERE "Motor" LIKE '%V8%') AS Motor_V8,

	(SELECT ROUND(AVG("Velocidade_Maxima"), 2)
	FROM cars_db_tratado
	WHERE "Motor" LIKE '%V12%') AS Motor_V12,
	
	(SELECT ROUND(AVG("Velocidade_Maxima"), 2)
	FROM cars_db_tratado
	WHERE "Motor" LIKE '%Inline-4%') AS Motor_Inline4,

	(SELECT ROUND(AVG("Velocidade_Maxima"), 2)
	FROM cars_db_tratado
	WHERE "Motor" LIKE '%I4%') AS Motor_I4;

