# 🦋 AUTOMAT – Suite d'automatisation Bluesky basée sur le code réel des meilleurs projets

Ce dépôt **ne réinvente pas la roue**. Il regroupe et organise le **code réel et éprouvé** des meilleurs projets open-source d'automatisation Bluesky.

## Sources intégrées

| Module | Source originale | Description |
|--------|------------------|-----------|
| `modules/scheduled-post` | [philnash/bsky-bot](https://github.com/philnash/bsky-bot) | Bot TypeScript + GitHub Actions pour poster selon un planning |
| `modules/firehose-bot` | [bluesky-hack/bot](https://github.com/bluesky-hack/bot) | Bot Python qui écoute le firehose en temps réel + exemples cron |
| `modules/rss-bot` | [joschi/blueskyfeedbot](https://github.com/joschi/blueskyfeedbot) | Action GitHub pour poster automatiquement des flux RSS |
| `modules/engagement` | [Endless-Range/bluesky-engagement-bot](https://github.com/Endless-Range/bluesky-engagement-bot) | Bot d'engagement complet (recherche mots-clés, like, repost, réponses avec IA) |

Tous les crédits vont aux auteurs originaux. Le code a été copié et organisé ici pour te permettre d'avoir **tout au même endroit**, prêt à l'emploi.

---

## Structure

```
AUTOMAT/
├── modules/
│   ├── scheduled-post/     ← Code de philnash/bsky-bot (TypeScript)
│   ├── firehose-bot/       ← Code de bluesky-hack/bot (Python)
│   ├── rss-bot/            ← Code de joschi/blueskyfeedbot (TypeScript / GitHub Action)
│   └── engagement/         ← Code de Endless-Range/bluesky-engagement-bot (Python)
├── .env.example
└── README.md
```

---

## Comment démarrer rapidement

### 1. Configurer les credentials

```bash
cp .env.example .env
```

Remplis :
```env
BLUESKY_HANDLE=tonhandle.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

Crée une App Password ici : https://bsky.app/settings/app-passwords

### 2. Choisir un module et suivre son README

Chaque dossier dans `modules/` contient le code original + les instructions d'utilisation du projet source.

---

## Recommandations d'usage

| Objectif | Module à utiliser |
|----------|-------------------|
| Poster automatiquement selon un horaire | `modules/scheduled-post` (philnash) |
| Poster un flux RSS | `modules/rss-bot` (joschi) |
| Répondre en temps réel aux mentions / mots-clés | `modules/firehose-bot` (bluesky-hack) |
| Engagement intelligent (like + repost + réponses IA) | `modules/engagement` (Endless-Range) |

---

## Crédits

- **philnash** – [bsky-bot](https://github.com/philnash/bsky-bot)
- **bluesky-hack** – [bot](https://github.com/bluesky-hack/bot)
- **joschi** – [blueskyfeedbot](https://github.com/joschi/blueskyfeedbot)
- **Endless-Range** – [bluesky-engagement-bot](https://github.com/Endless-Range/bluesky-engagement-bot)

Merci à eux pour le travail open-source de qualité.
