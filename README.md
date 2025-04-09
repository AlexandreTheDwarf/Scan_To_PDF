```markdown
# 📚 Scan to PDF

Un petit script Python pour **télécharger automatiquement des chapitres de mangas depuis anime-sama.fr** et les convertir **en fichiers PDF**, rangés proprement dans un dossier au nom du manga.

---

## ✅ Fonctionnalités

- Télécharge automatiquement les pages d’un ou plusieurs chapitres.
- Regroupe chaque chapitre dans un **fichier PDF**.
- Range les PDF dans un dossier unique avec le **nom propre du manga** (espaces au lieu de `%20`).
- Supprime les images après génération du PDF pour garder le dossier propre.

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

3. Il te demandera :
   ```
   Entrez le chapitre de début : 1
   Entrez le chapitre de fin : 3
   ```

4. Résultat :
   ```
   output/
   └── Chainsaw man/
       ├── chapitre_1.pdf
       ├── chapitre_2.pdf
       └── chapitre_3.pdf
   ```

---

## 🧰 Pré-requis

- Python 3.10+
- Modules Python :
  - `requests`
  - `img2pdf`
  - `PyPDF2`

Installe-les rapidement :
```bash
pip install requests img2pdf PyPDF2
```

---

## 📁 Structure du projet

```
Scan_To_PDF/
├── main.py
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

---

## 📝 Licence

Libre d’utilisation et de modification. Améliore-le à ta sauce !
```

---
