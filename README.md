# kyroz.app — site de présentation

Site vitrine statique de Kyroz. Une seule page, aucun build, aucune dépendance.

**En ligne :** https://kyroz.app

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | La page. Tout est dedans (CSS inclus, logo en SVG inline). |
| `legal.html` | Confidentialité + conditions d'utilisation. **Généré** depuis `Kyroz-app` (`constants/legal.ts`) — ne pas éditer à la main. |
| `fonts/inter-latin.woff2` | Police Inter, hébergée ici (pas chez Google Fonts — voir « Sécurité »). |
| `favicon.svg` | Icône d'onglet, couleur adaptative clair/sombre. |
| `favicon.ico` | Icône de la barre d'adresse (16/32/48 px). **À la racine, obligatoire.** |
| `favicon-32.png` | Repli PNG pour les vieux navigateurs. |
| `apple-touch-icon.png` | Icône « ajouter à l'écran d'accueil » (180x180). |
| `og-image.png` | Aperçu au partage du lien. |
| `app-store-badge.svg` | Badge officiel « Télécharger dans l'App Store ». **Ne pas modifier.** |
| `tools/make-favicon.py` | Regénère `favicon.ico` + `favicon-32.png`. |
| `CNAME` | Dit à GitHub Pages de servir le site sur `kyroz.app`. **Ne pas supprimer.** |
| `_config.yml` | Réglages de publication : sert `.well-known/`, ne publie pas `README.md`, `tools/`, `og-image.svg`. |
| `.well-known/security.txt` | Contact pour signaler une faille. **Date `Expires` à repousser avant le 2027-09-18.** |

## Publier une modification

Modifier le fichier, puis dans GitHub Desktop : **Commit** → **Push**.
Le site se met à jour tout seul en ~1 minute.

## Les stores

**App Store : en ligne depuis le 2026-09-12** — https://apps.apple.com/fr/app/kyroz/id6796427402.
Le badge, le bouton « Télécharger » de la barre du haut (`nav-cta`) et les
descriptions de partage le disent déjà.

Le badge est le **visuel officiel** d'Apple (`app-store-badge.svg`, version noire,
en français), téléchargé depuis leur outil marketing le 2026-09-15. Leurs règles de
marque interdisent de le redessiner ou de le recolorer : on change sa taille, rien d'autre.

### Le jour du lancement sur Google Play

Dans `index.html`, chercher `store-badge is-soon` — il ne reste que le badge Google Play :

```html
<!-- AVANT (badge « bientôt », non cliquable) -->
<span class="store-badge is-soon" role="link" aria-disabled="true" ...>

<!-- APRÈS (badge cliquable) -->
<a class="store-badge" href="https://play.google.com/store/apps/details?id=...">
```

Penser aussi à :
- remplacer `Bientôt sur` par `Disponible sur` dans le badge, et le visuel officiel Google ;
- passer la pastille du hero (« Disponible sur iOS ») et la note sous les badges à iOS **et** Android ;
- remettre « iOS et Android » dans les trois `description` du `<head>`.

## Sécurité

Audit du 2026-09-18. Les règles à garder :

- **Aucune ressource externe.** Tout est servi depuis `kyroz.app` — police comprise.
  Charger Google Fonts (ou un CDN, un outil de stats) envoie l'IP des visiteurs à un
  tiers sans consentement (RGPD/CNIL), et la CSP le bloquerait de toute façon.
- **CSP en balise `<meta>`** dans le `<head>` des deux pages (GitHub Pages ne permet
  aucun en-tête HTTP). `index.html` n'a **aucun script** (`script-src 'none'`) : en
  ajouter un demande de modifier la CSP. Celle de `legal.html` autorise son unique
  script par empreinte sha256, calculée par le générateur de l'app.
- **Branche `main` protégée** : pas de force-push ni de suppression.
- **Domaine `kyroz.app` vérifié** dans GitHub (Settings → Pages). Garder le TXT
  `_github-pages-challenge-brgkevin-arch` dans Cloudflare.
- **DNS (Cloudflare)** : DMARC en `p=quarantine`, CAA `letsencrypt.org`.
- **Sous-domaine vers GitHub Pages** : activer d'abord Pages avec le domaine dans le
  dépôt, **puis** créer le CNAME. Et le supprimer si le site s'arrête : un CNAME qui
  pointe vers un Pages que personne ne réclame peut être pris par n'importe qui
  (c'est arrivé à `kadenz.kyroz.app`, corrigé le 2026-09-18).

## Note

Le code source de l'app vit dans un autre dépôt : `brgkevin-arch/Kyroz-app`.

## Régénérer l'image de partage (`og-image.png`)

`og-image.png` est l'aperçu qui s'affiche quand le lien est partagé (WhatsApp,
iMessage, X…). Il est fabriqué à partir de `og-image.svg`.

Si tu modifies le SVG, relance ces deux commandes depuis ce dossier :

```bash
qlmanage -t -s 1200 -o . og-image.svg && sips -c 630 1200 og-image.svg.png --out og-image.png && rm og-image.svg.png
```

Le canevas du SVG est carré à dessein (l'outil macOS force une sortie carrée) ;
le recadrage central le ramène au 1200x630 attendu par les réseaux sociaux.

## Regénérer les favicons

```bash
python3 tools/make-favicon.py
```

Pas de dépendance à installer : le script dessine lui-même les polygones de la
marque et écrit le PNG/ICO. Un convertisseur classique aurait aplati la
transparence sur du blanc, ce qui remettrait un carré blanc autour du logo.

⚠️ Les navigateurs mettent les favicons en cache très longtemps, bien au-delà des
en-têtes HTTP. Si tu changes l'icône sans changer le nom du fichier, tu peux
continuer à voir l'ancienne pendant des jours. Renomme le fichier pour forcer.
