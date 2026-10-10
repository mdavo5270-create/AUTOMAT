# 🐛 AUTOMAT — Automatisation Bluesky 24/7

Suite d'automatisation **prête à l'emploi** qui tourne **sans intervention humaine** grâce à **GitHub Actions**.

Code adapté à partir de :
- [philnash/bsky-bot](https://github.com/philnash/bsky-bot)
- [bluesky-hack/bot](https://github.com/bluesky-hack/bot)
- [joschi/blueskyfeedbot](https://github.com/joschi/blueskyfeedbot)
- [Endless-Range/bluesky-engagement-bot](https://github.com/Endless-Range/bluesky-engagement-bot)

---

## Déploiement 24/7 (obligatoire — 2 minutes)

### 1. Ajoute les secrets GitHub

Va dans ton dépôt → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Obligatoire | Valeur |
|--------|-------------|--------|
| `BLUESKY_HANDLE` | Oui | `tonhandle.bsky.social` |
| `BLUESKY_APP_PASSWORD` | Oui | App Password (https://bsky.app/settings/app-passwords) |
| `KEYWORDS` | Non | `python,bluesky,ia` |
| `RSS_FEED` | Non | URL de ton flux RSS |
| `POST_TEXT` | Non | Texte du post programmé |

### 2. Active les workflows

Onglet **Actions** → active les workflows s'ils sont désactivés.

### 3. C'est tout

Les bots tournent automatiquement :

| Workflow | Fréquence |
|----------|-----------|
| **RSS** | Toutes les 2 heures |
| **Engagement (likes)** | 4	imes / jour |
| **Réponses mentions** | Toutes les heures |
| **Post programmé** | 09:30 et 18:30 UTC |

Tu peux aussi les lancer manuellement (bouton **Run workflow**).

---

## Modules locaux (optionnel)

```bash
git clone https://github.com/mdavo5270-create/AUTOMAT.git
cd AUTOMAT
pip install -r requirements.txt
cp .env.example .env   # remplis BLUESKY_HANDLE + BLUESKY_APP_PASSWORD

python -m automat.post --text "Test"
python -m automat.rss --feed https://exemple.com/rss --max 2
python -m automat.engage
python -m automat.replies
```

---

## Important

- Utilise **toujours** une **App Password**, jamais ton vrai mot de passe.
- GitHub Actions = hébergement gratuit 24/7 pour les tâches planifiées.
- Le firehose temps réel (connexion permanente) nécessite un VPS ; les workflows ci-dessus couvrent 95 % des besoins d'automatisation sans serveur.

Dépôt : https://github.com/mdavo5270-create/AUTOMAT
