---
exportFilename: slides
---


# **iFoodDB** - A Food Database

Par Romain Croughs, Chris Eid, Gabriel Goldsztajn, et Lucas Van Praag.

`INFO-H-303` - Bases de données - 2023-2024

---

## Table des matières

<Toc/>

---

## Introduction

### Technologies utilisées

- <bxl-python/> Python
- <bxl-postgresql/> PostgreSQL

---

## Architecture de la base de données

<div class="flex justify-center items-center h-full">
  <img src="/diagram.png" class="rounded shadow w-3/4 h-3/4 object-contain " alt="Architecture de la base de données"/>
</div>

---

## Méthodes d'extraction des données

- JSON: Utilsation de la librairie `json` de Python pour lire les données.
- TSV: Utilisation de la librairie `csv` de Python pour lire les données, sauf que le délimiteur est `\t`.
- XML: Utilisation de la librairie `xml.etree.ElementTree` de Python pour lire les données.

Utilisation d'une classe `Extractor` qui contient des méthodes telles que:

- `extract_restaurants(tsv_path: str) -> list[Restaurant]`
- `extract_users(json_path: str) -> list[User]`
- `extract_comments(xml_path: str) -> list[Comment]`

---

### Prenons l'exemple de la méthode `extract_comment`

Le TSV est le fichier le plus compliqué à parser, car il ne contient pas de balises claires comme le XML ou le JSON, nous devons donc statiquement définir les colonnes et les lire une par une.

La méthode `extract_comment` permet de parser une ligne d'un fichier TSV et de retourner un objet `Comment`.

---

```python
def extract_comment(self, comment) -> Comment:
        com = comment[0]
        note = comment[1]
        date = comment[2]
        recommendation = 0
        if comment[3] == "recommandé":
            recommendation = Recommendation.RECOMMENDED
        elif comment[3] == "déconseillé":
            recommendation = Recommendation.NOT_RECOMMENDED
        elif comment[3] == "à éviter d'urgence":
            recommendation = Recommendation.TO_BE_AVOIDED
        else:
            print(comment[3])
        restaurant = comment[4]
        noteservice = None
        notedelivery = None
        if comment[5][0] == "H":
            noteservice = int(comment[5][-1])
        else :
            notedelivery = int(comment[5][-1])

        datecomm = comment[6]
        menu = comment[7].split(';')
        price = float(comment[8])
        begin = int(comment[9])
        end = int(comment[10])
        user = comment[11]
        return Comment(user, com, datecomm, restaurant, note, date, menu, price, begin, end, recommendation, noteservice, notedelivery)
```

---

## Requêtes SQL demandées

### Requête 1
