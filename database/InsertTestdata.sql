USE stud_v23_tda072;


SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE admin;
TRUNCATE TABLE quiz;
TRUNCATE TABLE quiz_sesjon;
TRUNCATE TABLE spørsmål;
TRUNCATE TABLE spørsmål_har_quiz;
TRUNCATE TABLE spørsmålskategori;
TRUNCATE TABLE svarmulighet;

SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO admin (login, passord, fornavn, etternavn) VALUES
	('Tetiana', 'pbkdf2:sha256:260000$nrT5KAfL8aYlThOj$b435183950cf953d3ff0e7b45af0f75929b32ea31a0ee7f2c1150400213f0cd7', 'Tetiana', 'Verk'),
    ('ylu002@uit.no', 'pbkdf2:sha256:260000$2OdEg0WIyuBjEKka$9d6d1f0e745fd94e65f20aa2ce5ea5b476a414d7038f66964406ceb81635b432', 'Yue', 'Luo');
 
 
INSERT INTO spørsmålskategori (navn) VALUES ('Sport'), ('Geografi'), ('Historie'), ('Musikk'), ('Kino'), ('Mat og drikke');

  
INSERT INTO spørsmål (spørsmål, kategori_id, admin_id) VALUES
('Hvilken bergart er steinene i curling alltid laget av?', 1, 2), 
('Hvor mange mål scorte Ole Gunnar Solskjær for Manchester United?', 1, 2),
('Hva heter Serena Williams tennisspillende søster?', 1, 2), 
('Hva heter verdens nest største innsjø?', 2, 2),
('Hva heter verdens nest største elv med tanke på vannføring?', 2, 2),
('Hvilket land vant Fotball VM i 2010?', 1, 2),
('For hvilket lag spilte Michael Jordan mesteparten av karrieren?', 1, 2),
('Hva heter Norges nordligste punkt?', 2, 2),
('Hva heter det tredje høyeste fjellet i verden?', 2, 2),
('I hvilket land startet man å dyrke bananer?', 2, 2),
('Hvem av disse har vært statsminister i Norge?', 3, 2),
('D.D.E ga ut «Rompa mi» i 1996. Hvor kommer dette trønderbaserte bandet fra?', 4, 2),
('Hvem av disse skuespillerne er dubbet i Flåklypa grand prix?', 5, 2),
('Hva kalte man ølet som vikingene pleide å brygge?', 6, 2);


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
	('Kunnskapsduellen', 'Kunnskapsduellen. Hva vet du egentlig? Quiz_1 av Yue', 2), 
    ('Quizmania', 'Hvor mye kan du om Sport og Geografi? Quiz_2 av Yue', 2), 
    ('Quizmaster', 'Quizmaster: Den store kunnskapstesten. Quiz_3 av Yue', 2);


INSERT INTO spørsmål_har_quiz (spørsmål_id, quiz_id) VALUES
	(1, 1), (2, 1), (3, 1), (4, 1),(5, 1),
    (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), 
    (11, 3), (12, 3), (13, 3), (14, 3);
    
    
INSERT INTO quiz_sesjon (spørsmål_har_quiz_id, svar_id) VALUES
	(1, 3), (2, 6), (3, 10), (4, 16), (5, 19),
    (1, 2), (2, 5), (3, 12), (4, 14), (5, 19),
    (1, 3), (2, 7), (3, 10), (4, 14), (5, 19),
    (6, 23), (7, 25), (8, 29), (9, 35), (10, 37), 
    (6, 23), (7, 26), (8, 30), (9, 35), (10, 40), 
    (11, 42), (12, 47), (13, 54), (14, 56), 
    (11, 44), (12, 49), (13, 52), (14, 58);

    