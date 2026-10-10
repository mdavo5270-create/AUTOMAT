# 🦋 AUTOMAT – Suite d'automatisation Bluesky prête à l'emploi

**AUTOMAT** est une suite complète et modulaire pour automatiser presque tout sur Bluesky :

- 📅 Posts programmés
- 📡 Publication automatique depuis un flux RSS
- 💬 Réponses automatiques aux mentions
- ❤️ Engagement intelligent (like / repost selon mots-clés)
- 🤖 Génération de contenu avec IA (optionnel)
- 🧹 Nettoyage de vieux posts

Inspiré des meilleurs projets open-source (philnash/bsky-bot, bluesky-hack/bot, joschi/blueskyfeedbot, Endless-Range/bluesky-engagement-bot, etc.) et unifié dans un seul outil simple à utiliser.

---

## 🚀 Installation rapide

### 1. Cloner le dépôt
```bash
git clone https://github.com/mdavo5270-create/AUTOMAT.git
cd AUTOMAT
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer les secrets
```bash
cp .env.example .env
```

Édite `.env` et remplis :
```env
BLUESKY_HANDLE=tonhandle.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx   # Crée une App Password ici : https://bsky.app/settings/app-passwords
```

> **Important** : utilise toujours une **App Password**, jamais ton vrai mot de passe.

---

## 📦 Modules disponibles

| Module | Commande | Description |
|--------|----------|-------------|
| **Post programmé** | `python -m automat.post` | Poster un message (texte + image optionnelle) |
| **RSS → Bluesky** | `python -m automat.rss` | Publie automatiquement les nouveaux articles d'un flux RSS |
| **Réponses auto** | `python -m automat.replies` | Répond aux mentions selon des règles |
| **Engagement** | `python -m automat.engage` | Like / Repost des posts contenant certains mots-clés |
| **Nettoyage** | `python -m automat.cleanup` | Supprime les vieux posts (selon âge) |

---

## ⚙️ Utilisation avec GitHub Actions (recommandé – 100 % gratuit)

Le dépôt contient déjà des workflows prêts à l'emploi dans `.github/workflows/`.

1. Va dans **Settings → Secrets and variables → Actions**
2. Ajoute les secrets :
   - `BLUESKY_HANDLE`
   - `BLUESKY_APP_PASSWORD`
3. Active les workflows dans l'onglet **Actions**

Tu peux modifier les horaires dans les fichiers YAML (syntaxe cron).

---

## 🛠️ Structure du projet

```
AUTOMAT/
├── automat/                 # Code principal
│   ├── __init__.py
│   ├── client.py            # Client Bluesky unifié
│   ├── post.py              # Module de posting
│   ├── rss.py               # Module RSS
│   ├── replies.py           # Réponses automatiques
│   ├── engage.py            # Engagement
│   └── cleanup.py           # Nettoyage
├── .github/workflows/       # Automatisation GitHub Actions
├── config/                  # Configurations exemples
├── .env.example
├── requirements.txt
└── README.md
```

---

## 💡 Exemples de configuration

### Poster un message simple
```bash
python -m automat.post --text "Bonjour Bluesky 🦋"
```

### Poster depuis un RSS toutes les heures
Modifie `config/rss.yaml` puis lance :
```bash
python -m automat.rss
```

### Engagement sur des mots-clés
Dans `config/engage.yaml` :
```yaml
keywords:
  - "python"
  - "automatisation"
  - "bluesky"
actions:
  like: true
  repost: false
max_per_hour: 15
```

---

## 🔒 Sécurité

- Utilise toujours des **App Passwords**
- Ne commit jamais ton fichier `.env`
- Les rate limits de Bluesky sont respectés automatiquement

---

## 📚 Sources d'inspiration

Ce projet unifie et simplifie les idées des dépôts suivants :
- [philnash/bsky-bot](https://github.com/philnash/bsky-bot)
- [bluesky-hack/bot](https://github.com/bluesky-hack/bot)
- [joschi/blueskyfeedbot](https://github.com/joschi/blueskyfeedbot)
- [Endless-Range/bluesky-engagement-bot](https://github.com/Endless-Range/bluesky-engagement-bot)
- [skyware-js/bot](https://github.com/skyware-js/bot)
- SDK officiel `@atproto/api` et `atproto` (Python)

---

**Prêt à automatiser ?**
Clone → Configure → Lance.

Des questions ou envie d'ajouter un module ? Ouvre une issue !
