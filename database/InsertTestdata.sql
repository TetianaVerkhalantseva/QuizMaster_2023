USE stud_v23_tda072;


SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE bruker;
TRUNCATE TABLE quiz;
TRUNCATE TABLE spørsmål;
TRUNCATE TABLE spørsmål_har_quiz;
TRUNCATE TABLE spørsmålskategori;
TRUNCATE TABLE svarmulighet;

SET FOREIGN_KEY_CHECKS = 1;


INSERT INTO bruker (login, passord, fornavn, etternavn, admin) VALUES
    ('admin', 'pbkdf2:sha256:600000$c0N3iJF3xOmWgt8U$158e361490ee7f6dbf3fb9df74b7fd7ca73e29b3bffb21aceccb3b6c88cda58d', 'Admin', 'Lærer', 1),
    ('student', 'pbkdf2:sha256:600000$0sVkegcldPEjRBqE$23a13db754280e69861059580f0630c81ee62afae8e9e89a5bac76c5fadf8d1c', 'Student', 'Lærer', 0); 

 
INSERT INTO spørsmålskategori (navn) VALUES ('Sport'), ('Geografi'), ('Historie'), ('Musikk'), ('Kino'), ('Mat og drikke');

  
INSERT INTO spørsmål (spørsmål, kategori_id, admin_id) VALUES
('Hvilken bergart er steinene i curling alltid laget av?', 1, 1), 
('Hvor mange mål scorte Ole Gunnar Solskjær for Manchester United?', 1, 1),
('Hva heter Serena Williams tennisspillende søster?', 1, 1), 
('Hva heter verdens nest største innsjø?', 2, 1),
('Hva heter verdens nest største elv med tanke på vannføring?', 2, 1),
('Hvilket land vant Fotball VM i 2010?', 1, 1),
('For hvilket lag spilte Michael Jordan mesteparten av karrieren?', 1, 1),
('Hva heter Norges nordligste punkt?', 2, 1),
('Hva heter det tredje høyeste fjellet i verden?', 2, 1),
('I hvilket land startet man å dyrke bananer?', 2, 1),
('Hvem av disse har vært statsminister i Norge?', 3, 1),
('D.D.E ga ut «Rompa mi» i 1996. Hvor kommer dette trønderbaserte bandet fra?', 4, 1),
('Hvem av disse skuespillerne er dubbet i Flåklypa grand prix?', 5, 1),
('Hva kalte man ølet som vikingene pleide å brygge?', 6, 1),
('Hvilket land hadde dronninger gjennom hele 1900-tallet?', 3, 1);


INSERT INTO svarmulighet (svar, korrekt, spørsmål_id) VALUES
	('marmor', 0, 1), ('skifer', 0, 1), ('granitt', 1, 1), ('kleberstein', 0, 1), 
    ('126', 1, 2), ('110', 0, 2), ('120', 0, 2), ('132', 0, 2), 
    ('Michelle', 0, 3), ('Venus', 1, 3), ('Brooke', 0, 3), ('Nicole', 0, 3), 
    ('Victoriasjøen', 0, 4), ('Lake Superior', 1, 4), ('Huronsjøen', 0, 4), ('Store Slavesjø', 0, 4), 
    ('Mekong', 0, 5), ('Yangtze', 0, 5), ('Kongo', 1, 5), ('Negro', 0, 5), 
    ('Brazil', 0, 6), ('Frankrike', 0, 6), ('Spania', 1, 6), ('Italia', 0, 6),
    ('Los Angeles Lakers', 0, 7), ('Chicago Bulls', 1, 7), ('Miami Heat', 0, 7), ('New York Knicks', 0, 7),
    ('Nordkapp', 0, 8), ('Knivskjellodden', 1, 8), ('Lindesnes', 0, 8), ('Kapp Horn', 0, 8),
    ('Mont Blanc', 0, 9), ('K2', 0, 9), ('Kanchenjunga', 1, 9), ('Makalu', 0, 9),
    ('India', 1, 10), ('Vietnam', 0, 10), ('Thailand', 0, 10), ('Indonesia', 0, 10),
    ('Kristin Halvorsen', 0, 11), ('Jens Stoltenberg', 1, 11), ('Kjell Magne Bondevik', 1, 11), ('Carl I. Hagen', 0, 11), ('Ingen', 0, 11),
    ('Trondheim', 0, 12), ('Namsos', 1, 12), ('Steinkjer', 0, 12), ('Levanger', 0, 12),
    ('Leif Juster', 1, 13), ('Henki Kolstad', 1, 13), ('Wenche Foss', 1, 13), ('Helge Reiss', 1, 13), ('Ingen', 0, 13),
    ('Mølje', 0, 14), ('Tomtebrygg', 0, 14), ('Vikingbrygg', 0, 14), ('Mjød', 1, 14);


INSERT INTO quiz (navn, beskrivelse, admin_id) VALUES
	('Kunnskapsduellen', 'Kunnskapsduellen. Hva vet du egentlig? Quiz_1 av Admin', 1), 
    ('Quizmania', 'Hvor mye kan du om Sport og Geografi? Quiz_2 av Admin', 1), 
    ('Quizmaster', 'Quizmaster: Den store kunnskapstesten. Quiz_3 av Admin', 1);


INSERT INTO spørsmål_har_quiz (spørsmål_id, quiz_id) VALUES
	(1, 1), (2, 1), (3, 1), (4, 1),(5, 1),
    (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), 
    (11, 3), (12, 3), (13, 3), (14, 3), (15, 3);
    