INSERT INTO "user" (name, password, email) VALUES
    ('Romain', 'romain', 'rom2dm@hotmail.fr'),
    ('Marion', 'marion', 'delcambremarion@gmail.com'),
    ('Olivier', 'olivier',  'olivierpalis@gmail.com');

INSERT INTO alert (name, url) VALUES
    ('Jantes 5x114', 'https://www.leboncoin.fr/equipement_auto/offres/ile_de_france/?th=1&q=Jantes%205x114'),

    ('InterfaceRenaultPioneer', 'https://www.leboncoin.fr/annonces/offres/ile_de_france/occasions/?th=1&q=interface%20renault%20pioneer'),
    ('CA-R-PI_184', 'https://www.leboncoin.fr/annonces/offres/ile_de_france/occasions/?th=1&q=CA-R-PI.184'),
    ('500rdlc', 'https://www.leboncoin.fr/motos/offres/ile_de_france/occasions/?th=1&q=500%20rdlc&it=1'),
    ('BarilletScenic2', 'https://www.leboncoin.fr/equipement_auto/offres/ile_de_france/occasions/?th=1&q=barillet%20scenic%202&it=1'),
    ('PiecesSupraMk3', 'https://www.leboncoin.fr/equipement_auto/offres/ile_de_france/occasions/?o=2&q=toyota%20supra%20mk3'),
    ('PiecesSupraMkIII', 'https://www.leboncoin.fr/equipement_auto/offres/ile_de_france/occasions/?o=2&q=toyota%20supra%20mkIII'),
    ('VolantSupraMk3', 'https://www.leboncoin.fr/equipement_auto/offres/ile_de_france/occasions/?th=1&q=volant%20toyota%20supra%20mk3'),
    ('Console_Centrale_Scenic', 'https://www.leboncoin.fr/equipement_auto/offres/ile_de_france/?th=1&q=console%20centrale%20scenic%202&it=1'),
    ('Ronax_500', 'https://www.leboncoin.fr/motos/offres/?th=1&q=Ronax%20500'),
    ('ergobaby', 'https://www.leboncoin.fr/annonces/offres/ile_de_france/?th=1&q=ergobaby&it=1'),

    ('Revoltech', 'https://www.leboncoin.fr/annonces/offres/ile_de_france/?th=1&q=Revoltech'),
    ('Hot toys', 'https://www.leboncoin.fr/annonces/offres/ile_de_france/?th=1&q=Hot%20toys'),
    ('Marvel', 'https://www.leboncoin.fr/annonces/offres/ile_de_france/?th=1&q=Marvel%20legends'),
    ('Mezco', 'https://www.leboncoin.fr/annonces/offres/?th=1&q=Mezco')
;

INSERT INTO subscription (id_alert, id_user) VALUES
    (1, 1),

    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (6, 2),
    (7, 2),
    (8, 2),
    (9, 2),
    (10, 2),
    (11, 2),

    (12, 3),
    (13, 3),
    (14, 3),
    (15, 3)
;
