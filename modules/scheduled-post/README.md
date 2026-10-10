# Module scheduled-post

**Source originale :** [philnash/bsky-bot](https://github.com/philnash/bsky-bot)

Bot TypeScript prêt à l'emploi pour poster automatiquement sur Bluesky selon un planning (via GitHub Actions).

## Utilisation

1. Installe les dépendances :
```bash
cd modules/scheduled-post
npm install
```

2. Configure les variables d'environnement (`BSKY_HANDLE` et `BSKY_PASSWORD`).

3. Modifie `src/lib/getPostText.ts` pour générer le texte de ton post.

4. Lance :
```bash
npx tsx src/index.ts
```

Le workflow GitHub Actions original se trouve dans le dépôt source.
