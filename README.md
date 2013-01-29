Draaien van de applicatie (Noobproof guide)
===========================================

Hierbij hebben een werkende versie klaargezet met wat demo-code er in.

De installatie voor het draaien van een lokale instance van de software die via Sakai aangeroepen kan worden gaat als volgt:

    Installeer python 2.7 (http://www.python.org/getit/)
    Installeer python setuptools voor python 2.7 (http://pypi.python.org/pypi/setuptools#files)
    Voeg de subfolder "Scripts" van de python installatiefolder toe aan de omgevingsvariabele PATH (i.e.: "C:\Python27\Scripts")
    Als het goed is kan er nu via de commandline easy_install wordne aangeroepen om de benodigde packages te installeren
    Installeer de packages via de commandline met de volgende commando's:
        easy_install sqlalchemy
        easy_install flask
        easy_install oauth
        easy_install pyyaml
    Run de file flaskapplication.py met python (commando: python flaskapplication.py)
    Roep de tool aan via de sakai omgeving over poort 5000 (URL: localhost:5000)

Wij hebben een compatibele Sakai server staan op www.sakai.chozo.nl waarmee getest kan worden.
Inloggen kan hier met de acccounts: inst1, inst2, inst3, inst4, stud1, stud2, stud3, stud4.
Kies bovenin de subsite "Hurdygurdy" en ga vervolgens naar de pagina 'LTI' te vinden in de kantlijn
Als instructor kan hier een vraag gesteld worden en als student kunnen er vragen beantwoord worden
en geranked worden. Vervolgens kan de instructor dan zien welke vragen het hoogste gerate zijn

SWE_2013_Groep2
===============

Dit is de repository waar alle informatie die met iedereen gedeeld moet worden
terecht zal komen in de wiki. Evenals code die met iedereen gedeeld moet worden.

Ook komt na de sprints alle werkende code hier in te staan

Updating tussendoor
===================

Als je iets wilt toevoegen aan de wiki/code kan je een pull request doen
of aangeven (mail, issue, etc) dat je admin rights nodig hebt

