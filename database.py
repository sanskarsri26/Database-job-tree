import sqlite3

# Connect to (or create) the SQLite database
conn = sqlite3.connect('/Users/sanskarsrivastava/Desktop/CSE/Database-job/tree_data.db')
cursor = conn.cursor()

# Create the table (if it doesn't exist already)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tree_data (
        "Parcela_Site" TEXT,
        "nombre_colectores" TEXT,
        "fecha" TEXT,
        "parcela" INTEGER,
        "codigo_camara" TEXT,
        "numero_arbol" INTEGER,
        "nombre_archivo" TEXT,
        "especie_arbol" TEXT,
        "hora_cerrar_oruga" TEXT,
        "hora_abrir_oruga" TEXT,
        "arbol_sano" TEXT,
        "camara_con_termita" INTEGER,
        "diametro_arbol_cm" REAL,
        "temperatura" REAL,
        "presion_atmosferica_kpa" REAL,
        "notas" TEXT
    )
''')

# Insert the data into the table
cursor.execute('''
    INSERT INTO tree_data ("Parcela_Site", "nombre_colectores", "fecha", "parcela", "codigo_camara", 
    "numero_arbol", "nombre_archivo", "especie_arbol", "hora_cerrar_oruga", "hora_abrir_oruga", 
    "arbol_sano", "camara_con_termita", "diametro_arbol_cm", "temperatura", 
    "presion_atmosferica_kpa", "notas") 
    VALUES 
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 1, 'G2', 9019, '9019', 'Mauritia flexuosa', '09:55:30', '10:01:30', 'si', 'no', 30.4, 28.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 1, 'G2', 9019, '9019-2', 'Mauritia flexuosa', '10:02:05', '10:08:05', 'si', 'no', 31.8, 28.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 1, 'G2', 9020, '9020', 'Mauritia flexuosa', '10:10:30', '10:16:30', 'si', 'no', 23.6, 28.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 1, 'G2', 9020, '9020-2', 'Mauritia flexuosa', '10:19:10', '10:25:10', 'si', 'no', 26.7, 28.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 2, 'G2', 9053, '9053', 'Mauritia flexuosa', '10:30:50', '10:36:50', 'si', 'no', 30.2, 28.4, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 2, 'G2', 9053, '9053-2', 'Mauritia flexuosa', '10:38:05', '10:44:05', 'si', 'no', 30.5, 28.4, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 2, 'C4', 9061, '9061', 'Mauritia flexuosa', '10:47:30', '10:53:30', 'si', 'no', 18, 29.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 2, 'C4', 9061, '9061-2', 'Mauritia flexuosa', '11:59:50', '11:05:50', 'si', 'no', 20.3, 29.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 3, '', 9090, '9090', 'Mauritia flexuosa', '', '', NULL,NULL ,NULL ,NULL ,NULL , 'muerto'),  
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 3, '', 9090, '9090-2', 'Mauritia flexuosa', '', '', NULL,NULL ,NULL ,NULL ,NULL , 'muerto'),     
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 3, 'G2', 9095, '9095', 'Mauritia flexuosa', '11:10:40', '11:16:40', 'si', 'no', 38.5, 29.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 3, 'G2', 9095, '9095-2', 'Mauritia flexuosa', '11:18:00', '11:24:00', 'si', 'no', 27.9, 29.3, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 4, 'C4', 9101, '9101', 'Casearia sp', '11:52:25', '11:58:25', 'si', 'no', 22.1, 29.7, 100.8, 'inclinado'),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 4, 'C4', 9101, '9101-2', 'Casearia sp', '12:00:15', '12:06:15', 'si', 'no', 22.4, 29.7, 100.8, 'inclinado'),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 4, 'C4', 9110, '9110', 'Tabebuia insignis', '11:34:00', '11:40:00', 'si', 'si', 22.4, 29, 100.35, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 4, 'C4', 9110, '9110-2', 'Tabebuia insignis', '11:42:00', '11:48:00', 'si', 'no', 25.6, 29, 100.35, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 5, 'C4', 9192, '9192', 'Tabebuia insignis', '12:26:40', '12:32:40', 'si', 'no', 18, 29, 100.35, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 5, 'C4', 9192, '9192-2', 'Tabebuia insignis', '12:34:40', '12:40:40', 'si', 'no', 20, 29, 100.35, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 5, 'G2', 9194, '9194', 'Mauritia flexuosa', '12:12:20', '12:18:20', 'si', 'si', 35.4, 28.7, 100.18, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 5, 'G2', 9194, '9194-2', 'Mauritia flexuosa', '12:19:00', '12:25:00', 'si', 'no', 38.2, 28.7, 100.18, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 6, 'C4', 9197, '9197', 'Tabebuia insignis', '12:48:20', '12:54:20', 'si', 'no', 15.8, 28.1, 100.13, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 6, 'C4', 9197, '9197-2', 'Tabebuia insignis', '12:55:45', '13:01:45', 'si', 'no', 17.6, 28.1, 100.13, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 6, 'C4', 9202, '9202', 'Tabebuia insignis', '13:05:50', '13:11:50', 'si', 'si', 24.6, 30.1, 100.1, 'tronco irregular'),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 6, 'C4', 9202, '9202-2', 'Tabebuia insignis', '13:15:00', '13:21:00', 'si', 'no', 28, 30.1, 100.1, 'tronco irregular'),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 7, 'C4', 9287, '9187', 'Mauritiella armata', '14:33:20', '14:39:20', 'si', 'no', 10.6, 29.9, 100.02, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 7, 'C4', 9287, '9287-2', 'Mauritiella armata', '14:39:40', '14:45:40', 'si', 'no', 11.5, 29.9, 100.02, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 7, 'C4', 9290, '9290', 'Casearia sp', '14:50:10', '14:56:10', 'si', 'si', 12.3, 24.2, 100.08, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 7, 'C4', 9290, '9290-2', 'Casearia sp', '14:57:00', '15:03:00', 'si', 'no', 14.1, 24.2, 100.08, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 8, 'C4', 9325, '9325', 'Symphonia globulifera', '15:10:05', '15:16:05', 'si', 'si', 28.4, 29.3, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 8, 'C4', 9325, '9325-2', 'Symphonia globulifera', '15:16:45', '15:22:45', 'si', 'no', 31.1, 29.3, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 9, 'C4', 9392, '9392', 'Tabebuia insignis', '08:50:40', '08:56:40', 'si', 'no', 13.8, 27.5, 100.37, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 9, 'G2', 9392, '9392-2', 'Tabebuia insignis', '09:05:50', '09:11:50', 'si', 'no', 13.9, 27.5, 100.37, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 9, 'C4', 9393, '9393', 'Tabebuia insignis', '08:35:10', '08:41:10', 'si', 'no', 16.8, 27.5, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 9, 'G2', 9393, '9393-2', 'Tabebuia insignis', '08:42:20', '08:48:20', 'si', 'no', 17.5, 27.5, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 10, 'C4', 9404, '9404', 'Mauritiella armata', '09:19:00', '09:25:00', 'si', 'no', 14, 28.7, 100.37, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 10, 'G2', 9404, '9404-2', 'Mauritiella armata', '09:26:00', '09:32:00', 'si', 'no', 20.5, 28.7, 100.37, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 10, 'C4', 9405, '9405', 'Mauritiella armata', '09:37:00', '09:43:00', 'si', 'si', 23.6, 28.5, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 10, 'C4', 9405, '9405-2', 'Mauritiella armata', '09:45:05', '09:51:05', 'si', 'no', 26.7, 28.5, 100.36, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 12, 'C4', 9485, '9485', 'Lacmellea sp', '16:19:05', '16:25:05', 'si', 'no', 14.7, 27.6, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 12, 'C4', 9485, '9485-2', 'Lacmellea sp', '16:25:40', '16:31:40', 'si', 'no', 18, 27.6, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 12, 'G2', 9488, '9488', 'Symphonia globulifera', '16:03:20', '16:09:20', 'si', 'no', 25.1, 26.7, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 12, 'G2', 9488, '9488-2', 'Symphonia globulifera', '16:11:00', '16:17:00', 'si', 'no', 28.3, 26.7, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 13, 'C4', 9493, '9493', 'Ficus maxima', '15:44:00', '15:50:00', 'si', 'si', 17.8, 26.7, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 13, 'C4', 9493, '9493-2', 'Ficus maxima', '15:52:00', '15:58:00', 'si', 'no', 20.3, 26.7, 99.98, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 13, 'C4', 9498, '9498', 'Mauritiella armata', '15:28:25', '15:34:25', 'si', 'no', 11.8, 29.6, 99.97, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 13, 'C4', 9498, '9498-2', 'Mauritiella armata', '15:35:50', '15:41:50', 'si', 'no', 14.3, 29.6, 99.97, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 15, 'C4', 9582, '9582', 'Tabebuia insignis', '13:54:00', '14:00:00', 'si', 'no', 18.5, 29.6, 99.97, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 15, 'C4', 9582, '9582-2', 'Tabebuia insignis', '14:03:05', '14:09:05', 'si', 'no', 17, 29.6, 99.97, ''),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 15, 'C4', 9578, '9583', 'Tabebuia insignis', '13:31:00', '13:37:00', 'si', 'si', 23, 30.4, 100.11, 'con larvas urticantes'),
('QUI_02', 'Franco Macedo, William Wallace', '2022-01-07', 15, 'C4', 9578, '9583-2', 'Tabebuia insignis', '13:42:50', '13:48:50', 'si', 'si', 28.1, 30.4, 100.11, 'con larvas urticantes')

''')

# Commit and close the connection
conn.commit()
conn.close()