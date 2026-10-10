# Module engagement

**Source originale :** [Endless-Range/bluesky-engagement-bot](https://github.com/Endless-Range/bluesky-engagement-bot)

Bot d'engagement complet :
- Recherche de posts par mots-clés
- Analyse avec Claude (Anthropic)
- Like / Repost / Réponses
- Mode approbation manuelle (Slack)
- Base de données pour éviter les doublons
- Rate limiting

## Fichiers inclus

- `bluesky_monitor_v2.py` → Point d'entrée principal
- `utils/config.py` → Gestion de la configuration

Pour le code complet (base de données, logger, retry, Slack, etc.), regarde le dépôt original.

## Utilisation

```bash
cd modules/engagement
pip install atproto python-dotenv
```

Configure `.env` puis :

```bash
python bluesky_monitor_v2.py --manual
```
