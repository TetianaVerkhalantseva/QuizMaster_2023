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
	('Hvilke av disse filmene spiller Nicolas Cage i?', 5, 1),
	('Hvor høyt er Eiffeltårnet i Paris?', 2, 1),
	('Hva kalte man ølet som vikingene pleide å brygge?', 6, 1),
	('Hva heter verdens nest største elv med tanke på vannføring?', 2, 1),
	('Hvem av disse skuespillerne er dubbet i Flåklypa grand prix?', 5, 1),
	('I hvilket land ligger hovedkontoret til flyselskapet Ryanair?', 2, 1),
	('Hvor mange mål scorte Ole Gunnar Solskjær for Manchester United?', 1, 1),
	('Hva heter Norges nordligste punkt?', 2, 1),
	('Hvilket land vant Fotball VM i 2010?', 1, 1),
	('Hva heter Serena Williams tennisspillende søster?', 1, 1), 
	('Hvilket land hadde dronninger gjennom hele 1900-tallet?', 3, 1),
	('Hva heter verdens nest største innsjø?', 2, 1),
	('Hvem av disse har vært statsminister i Norge?', 3, 1),
	('D.D.E ga ut «Rompa mi» i 1996. Hvor kommer dette trønderbaserte bandet fra?', 4, 1),
	('I hvilket land startet man å dyrke bananer?', 2, 1),
	('For hvilket lag spilte Michael Jordan mesteparten av karrieren?', 1, 1),
	('Hva heter det tredje høyeste fjellet i verden?', 2, 1);


INSERT INTO svarmulighet (svar, korrekt, spørsmål_id) VALUES
	('marmor', 0, 1), ('skifer', 0, 1), ('granitt', 1, 1), ('kleberstein', 0, 1), 
	('Top Gun', 0, 2), ('Con Air', 1, 2), ('Mission Impossible', 0, 2), ('Wild at Heart', 1, 2), ('Ingen', 0, 2),
	('Mølje', 0, 4), ('Tomtebrygg', 0, 4), ('Vikingbrygg', 0, 4), ('Mjød', 1, 4),
	('Mekong', 0, 5), ('Yangtze', 0, 5), ('Kongo', 1, 5), ('Negro', 0, 5),
	('Leif Juster', 1, 6), ('Henki Kolstad', 1, 6), ('Wenche Foss', 1, 6), ('Helge Reiss', 1, 6), ('Ingen', 0, 6),
	('126', 1, 8), ('110', 0, 8), ('120', 0, 8), ('132', 0, 8), 
	('Nordkapp', 0, 9), ('Knivskjellodden', 1, 9), ('Lindesnes', 0, 9), ('Kapp Horn', 0, 9),
	('Brazil', 0, 10), ('Frankrike', 0, 10), ('Spania', 1, 10), ('Italia', 0, 10),
	('Michelle', 0, 11), ('Venus', 1, 11), ('Brooke', 0, 11), ('Nicole', 0, 11), 
	('Victoriasjøen', 0, 13), ('Lake Superior', 1, 13), ('Huronsjøen', 0, 13), ('Store Slavesjø', 0, 13), 
	('Kristin Halvorsen', 0, 14), ('Jens Stoltenberg', 1, 14), ('Kjell Magne Bondevik', 1, 14), ('Carl I. Hagen', 0, 14), ('Ingen', 0, 14),
	('Trondheim', 0, 15), ('Namsos', 1, 15), ('Steinkjer', 0, 15), ('Levanger', 0, 15),
	('India', 1, 16), ('Vietnam', 0, 16), ('Thailand', 0, 16), ('Indonesia', 0, 16),
	('Los Angeles Lakers', 0, 17), ('Chicago Bulls', 1, 17), ('Miami Heat', 0, 17), ('New York Knicks', 0, 17),
	('Mont Blanc', 0, 18), ('K2', 0, 18), ('Kanchenjunga', 1, 18), ('Makalu', 0, 18);


INSERT INTO quiz (navn, beskrivelse, admin_id) VALUES
	('Kunnskapsduellen', 'Den store kunnskapstesten. Quiz_1 av Admin', 1), 
	('Quizmania', 'Hva vet du egentlig? Quiz_2 av Admin', 1), 
	('Quizmaster', 'Megaquiz om alt mellom himmel og jord: Quiz_3 av Admin', 1);


INSERT INTO spørsmål_har_quiz (spørsmål_id, quiz_id) VALUES
	(1, 1), (2, 1), (3, 1), (4, 1),(5, 1),
    (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), 
    (11, 3), (12, 3), (13, 3), (14, 3), (15, 3);
    