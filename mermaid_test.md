```mermaid
---
title
---
erDiagram
    FILMS {
        int4 film_id PK
        varchar titre
        varchar titre_original
        int4 score_presse
        int4 score_spectateur
        varchar annee
        int4 duree 
        varchar description 
        varchar public 
        varchar langue_origine 
    }
    SERIES {
        serie_id int4 PK
        varchar titre
        varchar titre_original
        int4 score_presse
        int4 score_spectateur
        varchar annee
        varchar duree
        varchar description
        varchar nombre_saisons
        varchar nombre_episodes
    }
    PERSONNES {
        int4 personnes_id PK
        varchar prenom
        varchar nom
    }
    FILMS_GENRES {
        int4 film_id PK, FK
        varchar genre PK
    }
    ORIGINE_GEO_FILMS{
        int4 film_id PK, FK
        varchar pays  PK
    }
    ACTEURS_FILMS {
        int4 film_id  PK,FK
        int4 personnes_id  PK
    }
    REALISATEUR_FILMS {
        int4 film_id PK, FK
        int4 personnes_id PK
    }
    SERIES_GENRE {
        int4 serie_id PK, FK
        varchar genre PK
    }
    ORIGINE_GEO_SERIES {
        int4 serie_id PK, FK
        varchar pays PK
    }
    ACTEURS_SERIES {
        int4 serie_id PK,FK
        int4 personnes_id PK
    }
    REALISATEUR_SERIES{
        int4 serie_id PK, FK
        int4 personnes_id PK
    }

    FILMS }|--|| FILMS_GENRES:has
    FILMS }|--|| ORIGINE_GEO_FILMS:has
    FILMS }|--|| ACTEURS_FILMS:has
    FILMS }|--|| REALISATEUR_FILMS:has
    SERIES }|--|| SERIES_GENRE:has
    SERIES }|--|| ORIGINE_GEO_SERIES:has
    SERIES }|--|| REALISATEUR_SERIES:has
    SERIES }|--|| ACTEURS_SERIES:has
    PERSONNES }|--|| ACTEURS_FILMS:has
    PERSONNES }|--|| REALISATEUR_FILMS:has
    PERSONNES }|--|| REALISATEUR_SERIES:has
    PERSONNES }|--|| ACTEURS_SERIES:has



    

