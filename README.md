# 🐛 AUTOMAT + OPTIMAT

Automatisation Bluesky **24/7** pour **@mdavo5270.bsky.social**.

## Deux couches

| Couche | Rôle |
|--------|------|
| **AUTOMAT** | Outils unitaires (post, RSS, likes, réponses) — déjà testés verts |
| **OPTIMAT** | **Méta-orchestrateur** : décide quoi lancer, te représente, fait le travail |

```
OPTIMAT (cerveau, 1×/heure)
   ├─ post intelligent (tips, questions, séries)
   ├─ RSS
   ├─ engagement (likes ciblés)
   ├─ réponses mentions
   ├─ stats + rapport hebdo
   └─ catalogue de 100 automatisations (active / stub)
```

## Déjà en place (24/7)

1. Workflows unitaires (post, RSS, engage, replies) — OK verts  
2. **OPTIMAT** — `.github/workflows/optomat.yml` chaque heure  
3. Catalogue des **100** idées dans `optomat/catalog.py`  
4. Contenu de représentation (tips / questions / séries) dans `optomat/brain.py`

## Activer OPTIMAT

1. Secrets déjà configurés (`BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD`)  
2. Actions → **OPTIMAT 24/7** → **Run workflow** (mode `auto` ou `full`)  
3. Vérifie ton profil : https://bsky.app/profile/mdavo5270.bsky.social

### Secrets optionnels

| Secret | Effet |
|--------|--------|
| `KEYWORDS` | Likes ciblés |
| `RSS_FEED` | Ton flux |
| `POST_TEXT` | Force un texte de post |
| `BRAND_SUFFIX` | Signature (défaut: `\u2014 via OPTIMAT 🐛`) |

## Les 100 automatisations

Tout n'est pas du code production en une fois (sinon spam + ban).  
OPTIMAT implémente le **cœur actif** et garde le reste en **stub** activable.

Voir :
- `optomat/catalog.py` — liste complète 1–100  
- `optomat/brain.py` — décisions  
- `optomat/worker.py` — exécution  

## Évolution

On active les stubs **un par un** selon ta niche (contenu, follows smart, IA, analytics…).

Commande locale :
```bash
pip install -r requirements.txt
python -m optomat.worker
```
