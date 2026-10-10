"""Catalogue des 100 automatisations — id, nom, catégorie, statut.
status: active | scheduled | stub
active = code réel exécuté par OPTIMAT
scheduled = déclenché via GitHub Actions / planning
stub = prêt à être branché (structure + config)
"""

CATALOG = [
    # A. Contenu & publication (1-20)
    {"id": 1, "name": "Post planifié", "cat": "content", "status": "active", "job": "post"},
    {"id": 2, "name": "Poster depuis RSS", "cat": "content", "status": "active", "job": "rss"},
    {"id": 3, "name": "Poster nouveautés blog/Substack", "cat": "content", "status": "scheduled", "job": "rss"},
    {"id": 4, "name": "Poster releases GitHub", "cat": "content", "status": "stub", "job": "github_release"},
    {"id": 5, "name": "Poster météo du jour", "cat": "content", "status": "stub", "job": "weather"},
    {"id": 6, "name": "Citation du jour", "cat": "content", "status": "active", "job": "quote"},
    {"id": 7, "name": "Image + légende planifiée", "cat": "content", "status": "stub", "job": "post_image"},
    {"id": 8, "name": "Threads automatiques", "cat": "content", "status": "stub", "job": "thread"},
    {"id": 9, "name": "Best-of de la semaine", "cat": "content", "status": "stub", "job": "bestof"},
    {"id": 10, "name": "Rappels d'événements", "cat": "content", "status": "stub", "job": "events"},
    {"id": 11, "name": "Stats personnelles", "cat": "content", "status": "active", "job": "stats_post"},
    {"id": 12, "name": "Résumé newsletter", "cat": "content", "status": "stub", "job": "newsletter"},
    {"id": 13, "name": "Cross-post Mastodon", "cat": "content", "status": "stub", "job": "cross_mastodon"},
    {"id": 14, "name": "Cross-post CMS/site", "cat": "content", "status": "stub", "job": "cross_cms"},
    {"id": 15, "name": "Offres d'emploi", "cat": "content", "status": "stub", "job": "jobs"},
    {"id": 16, "name": "Alertes status/incidents", "cat": "content", "status": "scheduled", "job": "rss"},
    {"id": 17, "name": "Anniversaires de posts", "cat": "content", "status": "stub", "job": "anniversary"},
    {"id": 18, "name": "Contenu saisonnier", "cat": "content", "status": "stub", "job": "seasonal"},
    {"id": 19, "name": "Questions récurrentes", "cat": "content", "status": "active", "job": "question"},
    {"id": 20, "name": "Post généré par IA", "cat": "content", "status": "stub", "job": "ai_post"},
    # B. Engagement (21-40)
    {"id": 21, "name": "Like par mots-clés", "cat": "engage", "status": "active", "job": "engage"},
    {"id": 22, "name": "Like niche", "cat": "engage", "status": "active", "job": "engage"},
    {"id": 23, "name": "Répondre aux mentions", "cat": "engage", "status": "active", "job": "replies"},
    {"id": 24, "name": "Répondre bienvenue", "cat": "engage", "status": "stub", "job": "welcome"},
    {"id": 25, "name": "Follow qui t'a liké", "cat": "engage", "status": "stub", "job": "follow_likers"},
    {"id": 26, "name": "Follow qui t'a reposté", "cat": "engage", "status": "stub", "job": "follow_reposters"},
    {"id": 27, "name": "Unfollow inactifs", "cat": "engage", "status": "stub", "job": "unfollow_inactive"},
    {"id": 28, "name": "Repost qualité niche", "cat": "engage", "status": "stub", "job": "repost_quality"},
    {"id": 29, "name": "Quote-post auto", "cat": "engage", "status": "stub", "job": "quote"},
    {"id": 30, "name": "Engager posts croissance", "cat": "engage", "status": "active", "job": "engage"},
    {"id": 31, "name": "Saluer nouveaux followers", "cat": "engage", "status": "stub", "job": "greet_followers"},
    {"id": 32, "name": "Réponse DM type", "cat": "engage", "status": "stub", "job": "dm_auto"},
    {"id": 33, "name": "Like commentaires sous tes posts", "cat": "engage", "status": "stub", "job": "like_comments"},
    {"id": 34, "name": "Engager tendances", "cat": "engage", "status": "stub", "job": "trends"},
    {"id": 35, "name": "Contenu starter packs", "cat": "engage", "status": "stub", "job": "starterpack"},
    {"id": 36, "name": "Relancer conversations", "cat": "engage", "status": "active", "job": "replies"},
    {"id": 37, "name": "Remercier reposts", "cat": "engage", "status": "stub", "job": "thanks_repost"},
    {"id": 38, "name": "Engager comptes hub", "cat": "engage", "status": "stub", "job": "hub_engage"},
    {"id": 39, "name": "Rate limit anti-spam", "cat": "engage", "status": "active", "job": "orchestrator"},
    {"id": 40, "name": "Rotation messages réponse", "cat": "engage", "status": "active", "job": "replies"},
    # C. Veille (41-55)
    {"id": 41, "name": "Surveiller mot-clé", "cat": "watch", "status": "active", "job": "engage"},
    {"id": 42, "name": "Alerte mot-clé", "cat": "watch", "status": "stub", "job": "alert_keyword"},
    {"id": 43, "name": "Posts populaires niche", "cat": "watch", "status": "stub", "job": "popular"},
    {"id": 44, "name": "Comptes qui parlent de ton sujet", "cat": "watch", "status": "stub", "job": "discover"},
    {"id": 45, "name": "Tendances Bluesky/ATProto", "cat": "watch", "status": "stub", "job": "trends_at"},
    {"id": 46, "name": "Archiver posts importants", "cat": "watch", "status": "stub", "job": "archive"},
    {"id": 47, "name": "Mentions marque/nom", "cat": "watch", "status": "active", "job": "replies"},
    {"id": 48, "name": "Veille concurrentielle", "cat": "watch", "status": "stub", "job": "competitors"},
    {"id": 49, "name": "Hashtags populaires", "cat": "watch", "status": "stub", "job": "hashtags"},
    {"id": 50, "name": "Comptes à suivre (bio)", "cat": "watch", "status": "stub", "job": "suggest_follow"},
    {"id": 51, "name": "Surveiller un handle", "cat": "watch", "status": "stub", "job": "watch_handle"},
    {"id": 52, "name": "Alerte compte important", "cat": "watch", "status": "stub", "job": "alert_account"},
    {"id": 53, "name": "Résumer firehose sujet", "cat": "watch", "status": "stub", "job": "firehose_summary"},
    {"id": 54, "name": "Threads longs populaires", "cat": "watch", "status": "stub", "job": "long_threads"},
    {"id": 55, "name": "Sentiment IA", "cat": "watch", "status": "stub", "job": "sentiment"},
    # D. Analytics (56-70)
    {"id": 56, "name": "Compter followers/jour", "cat": "analytics", "status": "active", "job": "stats"},
    {"id": 57, "name": "Graph évolution abonnés", "cat": "analytics", "status": "stub", "job": "graph"},
    {"id": 58, "name": "Top posts semaine", "cat": "analytics", "status": "stub", "job": "top_posts"},
    {"id": 59, "name": "Taux engagement/post", "cat": "analytics", "status": "stub", "job": "engagement_rate"},
    {"id": 60, "name": "Heures de pointe", "cat": "analytics", "status": "stub", "job": "peak_hours"},
    {"id": 61, "name": "Rapport hebdo auto", "cat": "analytics", "status": "active", "job": "weekly_report"},
    {"id": 62, "name": "Croissance mois/mois", "cat": "analytics", "status": "stub", "job": "mom_growth"},
    {"id": 63, "name": "Qui t'a unfollow", "cat": "analytics", "status": "stub", "job": "unfollowers"},
    {"id": 64, "name": "Nouveaux followers", "cat": "analytics", "status": "stub", "job": "new_followers"},
    {"id": 65, "name": "Score qualité post", "cat": "analytics", "status": "stub", "job": "quality_score"},
    {"id": 66, "name": "Export CSV activité", "cat": "analytics", "status": "stub", "job": "export_csv"},
    {"id": 67, "name": "Dashboard web", "cat": "analytics", "status": "stub", "job": "dashboard"},
    {"id": 68, "name": "Alerte chute abonnés", "cat": "analytics", "status": "stub", "job": "drop_alert"},
    {"id": 69, "name": "Stats par type contenu", "cat": "analytics", "status": "stub", "job": "by_type"},
    {"id": 70, "name": "Rapport ce qui a marché", "cat": "analytics", "status": "active", "job": "weekly_report"},
    # E. Modération (71-80)
    {"id": 71, "name": "Supprimer vieux posts", "cat": "mod", "status": "stub", "job": "cleanup_posts"},
    {"id": 72, "name": "Supprimer likes anciens", "cat": "mod", "status": "stub", "job": "cleanup_likes"},
    {"id": 73, "name": "Ignorer mots", "cat": "mod", "status": "stub", "job": "mute_words"},
    {"id": 74, "name": "Bloquer spammeurs", "cat": "mod", "status": "stub", "job": "block_spam"},
    {"id": 75, "name": "Mute mots toxiques", "cat": "mod", "status": "stub", "job": "mute_toxic"},
    {"id": 76, "name": "Nettoyer posts ratés", "cat": "mod", "status": "stub", "job": "cleanup_failed"},
    {"id": 77, "name": "Archiver puis supprimer", "cat": "mod", "status": "stub", "job": "archive_delete"},
    {"id": 78, "name": "Détecter bots bizarres", "cat": "mod", "status": "stub", "job": "detect_bots"},
    {"id": 79, "name": "Filtrer réponses par followers", "cat": "mod", "status": "active", "job": "replies"},
    {"id": 80, "name": "File d'approbation", "cat": "mod", "status": "stub", "job": "approval_queue"},
    # F. Infra (81-90)
    {"id": 81, "name": "GitHub Actions 24/7", "cat": "infra", "status": "active", "job": "orchestrator"},
    {"id": 82, "name": "VPS firehose", "cat": "infra", "status": "stub", "job": "firehose"},
    {"id": 83, "name": "Webhook → post", "cat": "infra", "status": "stub", "job": "webhook"},
    {"id": 84, "name": "Formulaire → post", "cat": "infra", "status": "stub", "job": "form"},
    {"id": 85, "name": "n8n/Make bridge", "cat": "infra", "status": "stub", "job": "n8n"},
    {"id": 86, "name": "Bot CLI", "cat": "infra", "status": "active", "job": "post"},
    {"id": 87, "name": "Multi-comptes", "cat": "infra", "status": "stub", "job": "multi"},
    {"id": 88, "name": "Backup PDS", "cat": "infra", "status": "stub", "job": "backup"},
    {"id": 89, "name": "Tests workflows", "cat": "infra", "status": "active", "job": "orchestrator"},
    {"id": 90, "name": "Logs + alertes échec", "cat": "infra", "status": "active", "job": "orchestrator"},
    # G. Croissance smart (91-100)
    {"id": 91, "name": "Tips récurrents", "cat": "growth", "status": "active", "job": "tip"},
    {"id": 92, "name": "Série 1 post/jour", "cat": "growth", "status": "active", "job": "series"},
    {"id": 93, "name": "Réponses semi-auto", "cat": "growth", "status": "active", "job": "replies"},
    {"id": 94, "name": "Collabs / mentions", "cat": "growth", "status": "stub", "job": "collab"},
    {"id": 95, "name": "Starter pack + accueil", "cat": "growth", "status": "stub", "job": "starter_welcome"},
    {"id": 96, "name": "Ressources gratuites", "cat": "growth", "status": "stub", "job": "resources"},
    {"id": 97, "name": "Threads valeur", "cat": "growth", "status": "stub", "job": "value_thread"},
    {"id": 98, "name": "Heures de pointe niche", "cat": "growth", "status": "active", "job": "orchestrator"},
    {"id": 99, "name": "Profil cohérent + posts alignés", "cat": "growth", "status": "active", "job": "series"},
    {"id": 100, "name": "Mesurer et itérer", "cat": "growth", "status": "active", "job": "weekly_report"},
]

def by_status(status: str):
    return [x for x in CATALOG if x["status"] == status]

def summary():
    from collections import Counter
    c = Counter(x["status"] for x in CATALOG)
    return dict(c)
