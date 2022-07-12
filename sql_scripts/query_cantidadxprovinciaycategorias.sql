select provincia, categoria, COUNT(*) as "numero registros" from datosconjuntos
GROUP BY provincia, categoria
order by provincia;