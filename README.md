# 📚 Scan to PDF

> ⚠️ **Disclaimer**  
> Ce script est fourni **uniquement à des fins éducatives**.  
> Son utilisation pour contourner des droits d’auteur ou accéder à du contenu protégé sans autorisation est **strictement interdite**.  
> L’auteur du script **décline toute responsabilité** en cas d’usage inapproprié ou illégal.

Un petit script Python pour **télécharger automatiquement des chapitres de mangas depuis anime-sama.fr** et les convertir **en fichiers PDF**, rangés proprement dans un dossier au nom du manga. Une interface graphique Tkinter est désormais disponible, et un exécutable est fourni pour simplifier l’utilisation.

---

## ✅ Fonctionnalités

- Télécharge automatiquement les pages d’un ou plusieurs chapitres.
- Regroupe chaque chapitre dans un **fichier PDF**.
- Range les PDF dans un dossier unique avec le **nom propre du manga** (espaces au lieu de `%20`).
- Supprime les images après génération du PDF pour garder le dossier propre.
- Interface graphique avec Tkinter pour une utilisation plus facile.
- Un fichier exécutable (`.exe`) est disponible dans le dossier `dist` pour une utilisation sans installation préalable de Python.

---

## 🧾 Exemple

Tu veux récupérer les chapitres 1 à 3 de *Chainsaw Man* :

1. Mets dans le code :
   ```python
   Anime_Name = "Chainsaw%20man"
   ```

2. Lance le script :
   ```bash
   python main.py
   ```

   Ou si tu utilises l'interface graphique :

   - Lance l'exécutable dans le dossier `dist/` ou ouvre `main.py` avec Python.
   - Entrez les informations nécessaires dans l'interface (nom de l'anime, chapitre de début et de fin).
   - Clique sur "Télécharger".

3. Résultat :
   ```
   output/
   └── Chainsaw man/
       ├── chapitre_1.pdf
       ├── chapitre_2.pdf
       └── chapitre_3.pdf
   ```

---

## 🧰 Pré-requis

Si tu utilises le script avec Python, voici les prérequis :

- Python 3.10+
- Modules Python :
  - `requests`
  - `img2pdf`
  - `PyPDF2`
  - `tkinter`

Installe-les rapidement :
```bash
pip install requests img2pdf PyPDF2
```

Si tu préfères utiliser l'exécutable, il te suffit de le lancer depuis le dossier `dist/` sans installation de Python.

---

## 📁 Structure du projet

```
Scan_To_PDF/
├── dist/                  # Contient l'exécutable (.exe)
│   └── Scan_to_PDF.exe
├── main.py                # Code source principal
├── output/                # Contient les PDFs, ignoré par Git
│   └── Chainsaw man/
│       ├── chapitre_1.pdf
│       └── chapitre_2.pdf
├── .gitignore
└── README.md
```

---

## 🛑 `.gitignore` recommandé

Crée un fichier `.gitignore` avec ceci :
```
output/
```

---

## ⚙️ Notes techniques

- Le nom de l’anime doit utiliser **`%20` pour les espaces** dans l’URL (ex: `Solo%20Leveling`) ;
- Ce `%20` est automatiquement converti en espace pour le nom du dossier local ;
- Les images sont téléchargées temporairement puis supprimées après génération du PDF.
- L'interface graphique Tkinter permet de lancer facilement le téléchargement en fournissant le nom de l'anime et les chapitres à télécharger.
- Le fichier exécutable dans le dossier `dist` permet de l'utiliser sans avoir besoin de Python installé.

---

## 📝 Licence

Ce projet est libre d’utilisation et de modification dans un cadre **légal et éthique**.  
Toute utilisation détournée est aux risques et périls de l'utilisateur, et **l’auteur décline toute responsabilité**.
