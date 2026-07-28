# kyroz.app — site de présentation

Site vitrine statique de Kyroz. Une seule page, aucun build, aucune dépendance.

**En ligne :** https://kyroz.app

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | La page. Tout est dedans (CSS inclus, logo en SVG inline). |
| `legal.html` | Confidentialité + conditions d'utilisation. |
| `kyroz-mark.svg` | Favicon (logo outline dark). |
| `CNAME` | Dit à GitHub Pages de servir le site sur `kyroz.app`. **Ne pas supprimer.** |

## Publier une modification

Modifier le fichier, puis dans GitHub Desktop : **Commit** → **Push**.
Le site se met à jour tout seul en ~1 minute.

## Le jour du lancement sur les stores

Dans `index.html`, chercher `store-badge`. Il y a deux blocs à changer :

```html
<!-- AVANT (badge « bientôt », non cliquable) -->
<span class="store-badge is-soon" role="link" aria-disabled="true" ...>

<!-- APRÈS (badge cliquable) -->
<a class="store-badge" href="https://apps.apple.com/app/idXXXXXXXXX">
```

Penser aussi à :
- remplacer `Bientôt sur` par `Télécharger sur` / `Disponible sur` dans les deux badges ;
- remplacer les icônes maison par les **visuels officiels** Apple et Google (leurs règles de marque l'imposent une fois l'app publiée) ;
- retirer le bandeau « Bientôt disponible » de la barre du haut (`nav-soon`) et le pastille « Bientôt sur iOS et Android » du hero.

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
