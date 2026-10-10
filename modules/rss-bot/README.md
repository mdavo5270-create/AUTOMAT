# Module rss-bot

**Source originale :** [joschi/blueskyfeedbot](https://github.com/joschi/blueskyfeedbot)

GitHub Action (et code TypeScript) qui publie automatiquement les nouveaux articles d'un flux RSS sur Bluesky.

## Utilisation recommandée

Utilise directement l'Action GitHub originale dans un workflow :

```yaml
- uses: joschi/blueskyfeedbot@v1
  with:
    rss-feed: https://ton-flux.com/rss
    template: |
      {{item.title}}
      {{item.link}}
    username: ${{ secrets.BLUESKY_USERNAME }}
    password: ${{ secrets.BLUESKY_PASSWORD }}
```

Le code source complet de l'Action est disponible ici pour référence et modification.
