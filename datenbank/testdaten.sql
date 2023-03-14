INSERT INTO
  finanzen.kategorie (id, name, farbe, maximal)
VALUES
  (1, 'Essen', 'is-danger', 180);

INSERT INTO
  finanzen.kategorie (id, name, farbe, maximal)
VALUES
  (2, 'Kleidung', 'is-warning', 300);

INSERT INTO
  finanzen.kategorie (id, name, farbe, maximal)
VALUES
  (3, 'Schule', 'is-info', 130);

INSERT INTO
  finanzen.ausgaben (grund, wert, datum, kategorie)
VALUES
  ('Döner', 5.9, '2023-03-01', 1);

INSERT INTO
  finanzen.ausgaben (grund, wert, datum, kategorie)
VALUES
  ('T-Shirt', 14, '2023-02-05', 2);

INSERT INTO
  finanzen.ausgaben (grund, wert, datum, kategorie)
VALUES
  ('Stifte', 12, '2023-02-07', 3);

INSERT INTO
  finanzen.ausgaben (grund, wert, datum, kategorie)
VALUES
  ('Socken', 12.33, '2023-03-11', 2);

INSERT INTO
  finanzen.ausgaben (grund, wert, datum, kategorie)
VALUES
  ('tolles Hemd', 87.54, '2023-03-14', 2);