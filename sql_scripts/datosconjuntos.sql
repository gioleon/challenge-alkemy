DROP TABLE IF EXISTS datosconjuntos;

CREATE TABLE datosconjuntos(
    cod_localidad VARCHAR(20),
    id_provincia VARCHAR(20),
    id_departamento INT,
    categoria VARCHAR(40),
    provincia VARCHAR(60),
    localidad VARCHAR(60),
    nombre VARCHAR(60),
    domicilio VARCHAR(60),
    codigo_postal VARCHAR(20),
    numero_de_telefono VARCHAR(15),
    mail VARCHAR(45),
    web VARCHAR(60),
    fecha_carga TIMESTAMP
)