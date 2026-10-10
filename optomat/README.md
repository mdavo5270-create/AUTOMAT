# OPTIMAT — L'automatisation qui gère les automatisations

OPTIMAT est le **cerveau** au-dessus d'AUTOMAT.

Il te **représente** sur Bluesky (`mdavo5270.bsky.social`) et décide, chaque heure, quoi faire :

- poster un tip / question / citation / série
- publier du RSS
- liker par mots-clés
- répondre aux mentions
- enregistrer des stats
- rapport hebdo

## Architecture

```
GitHub Actions (chaque heure)
        ↓
  optomat.brain   → décide les jobs selon l'heure
        ↓
  optomat.worker  → exécute (post, rss, engage, replies, stats…)
        ↓
  automat.*       → clients Bluesky déjà validés (verts)
```

## Catalogue 100

Voir `optomat/catalog.py` :
- **active** : exécuté maintenant
- **scheduled** : couvert par les workflows / RSS
- **stub** : structure prête, à activer une par une

## Lancer

```bash
python -m optomat.worker
```

Variables utiles :
- `OPTIMAT_MODE=auto|content|engage|full`
- `OPTIMAT_ONLY=post_smart,engage`
- `BRAND_SUFFIX` — signature en fin de post
- `KEYWORDS`, `RSS_FEED`, `POST_TEXT`

## Workflow

`.github/workflows/optomat.yml` — toutes les heures + bouton manuel.
