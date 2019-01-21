## Métadonnées d'un répertoire Git

- Auteur : Antoine Augusti <antoine.augusti@example.com>
- Schéma créé le : 12/31/18
- Site web : https://github.com/AntoineAugusti/data-codes-sources-fr
- Clé primaire : `repertoire_url`

### Modèle de données

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|nom|chaîne de caractères|Le nom du répertoire|nom-repertoire|Valeur obligatoire|
|organisation_nom|chaîne de caractères|Le nom de l'organisation|etalab|Valeur obligatoire|
|plateforme|chaîne de caractères|La plateforme de dépôt de code|GitHub|Valeur obligatoire, Valeurs autorisées : GitHub|
|repertoire_url|chaîne de caractères (format `uri`)|L'URL vers le répertoire|https://github.com/etalab/nom-repertoire|Valeur obligatoire|
|description|chaîne de caractères|La description du répertoire|Ce répertoire est utile|Valeur optionnelle|
|est_fork|booléen|Indique si le répertoire est un fork|false|Valeur obligatoire|
|date_creation|date et heure|La date de création du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|derniere_mise_a_jour|date et heure|La date de dernière mise à jour du répertoire|2018-12-01T20:00:55Z|Valeur obligatoire|
|page_accueil|chaîne de caractères|URL vers la page d'accueil du projet|https://etalab.gouv.fr|Valeur optionnelle|
|nombre_stars|nombre entier|Le nombre de fois où le répertoire a été ajouté aux favoris|42|Valeur obligatoire, Valeur minimale : 0|
|nombre_forks|nombre entier|Le nombre de fois où le répertoire a été forké|13|Valeur obligatoire, Valeur minimale : 0|
|licence|chaîne de caractères|La licence du répertoire, telle que détectée par la plateforme|MIT|Valeur optionnelle|
|nombre_issues_ouvertes|nombre entier|Le nombre d'issues actuellement ouvertes|0|Valeur obligatoire, Valeur minimale : 0|
|langage|chaîne de caractères|Le langage principal du répertoire, tel que détecté par la plateforme|Python|Valeur optionnelle|
|topics|chaîne de caractères|Les tags du répertoire|utile,france,opendata|Valeur optionnelle|
