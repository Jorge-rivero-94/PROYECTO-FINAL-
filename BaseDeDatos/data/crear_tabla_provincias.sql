CREATE TABLE IF NOT EXISTS provincias (
    codigo_ine SMALLINT UNSIGNED PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    codigo_comunidad SMALLINT UNSIGNED NOT NULL,
    FOREIGN KEY (codigo_comunidad) REFERENCES comunidades_autonomas(codigo_ine)
);

INSERT INTO provincias (codigo_ine, nombre, codigo_comunidad) VALUES
('01', 'Araba/Álava', '16'),
('02', 'Albacete', '08'),
('03', 'Alicante/Alacant', '10'),
('04', 'Almería', '01'),
('05', 'Ávila', '07'),
('06', 'Badajoz', '11'),
('07', 'Balears, Illes', '04'),
('08', 'Barcelona', '09'),
('09', 'Burgos', '07'),
('10', 'Cáceres', '11'),
('11', 'Cádiz', '01'),
('12', 'Castellón/Castelló', '10'),
('13', 'Ciudad Real', '08'),
('14', 'Córdoba', '01'),
('15', 'Coruña, A', '12'),
('16', 'Cuenca', '08'),
('17', 'Girona', '09'),
('18', 'Granada', '01'),
('19', 'Guadalajara', '08'),
('20', 'Gipuzkoa', '16'),
('21', 'Huelva', '01'),
('22', 'Huesca', '02'),
('23', 'Jaén', '01'),
('24', 'León', '07'),
('25', 'Lleida', '09'),
('26', 'Rioja, La', '17'),
('27', 'Lugo', '12'),
('28', 'Madrid', '13'),
('29', 'Málaga', '01'),
('30', 'Murcia', '14'),
('31', 'Navarra', '15'),
('32', 'Ourense', '12'),
('33', 'Asturias', '03'),
('34', 'Palencia', '07'),
('35', 'Palmas, Las', '05'),
('36', 'Pontevedra', '12'),
('37', 'Salamanca', '07'),
('38', 'Santa Cruz de Tenerife', '05'),
('39', 'Cantabria', '06'),
('40', 'Segovia', '07'),
('41', 'Sevilla', '01'),
('42', 'Soria', '07'),
('43', 'Tarragona', '09'),
('44', 'Teruel', '02'),
('45', 'Toledo', '08'),
('46', 'Valencia/València', '10'),
('47', 'Valladolid', '07'),
('48', 'Bizkaia', '16'),
('49', 'Zamora', '07'),
('50', 'Zaragoza', '02'),
('51', 'Ceuta', '18'),
('52', 'Melilla', '19');

SELECT
    p.nombre AS provincia,
    c.nombre AS comunidad_autonoma
FROM
    provincias p
JOIN
    comunidades_autonomas c ON p.codigo_comunidad = c.codigo_ine
ORDER BY
    p.nombre;