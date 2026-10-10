# Module firehose-bot

**Source originale :** [bluesky-hack/bot](https://github.com/bluesky-hack/bot)

Exemples de bots Python basés sur le SDK officiel `atproto`.

## Fichiers inclus

- `examples/cron-bot.py` → Poster selon un planning (APScheduler)
- `examples/firehose-bot.py` → Écouter le firehose en temps réel et répondre aux posts contenant un mot-clé

## Utilisation

```bash
cd modules/firehose-bot
pip install atproto python-dotenv apscheduler
```

Configure `.env` avec `BLUESKY_USERNAME` et `BLUESKY_PASSWORD`, puis :

```bash
python examples/cron-bot.py
# ou
python examples/firehose-bot.py
```
