import requests
import os
import re
from PyPDF2 import PdfMerger
import img2pdf
import tempfile

# Constantes
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output")

# Anime_Name avec '%20' pour l'URL, mais remplacement pour le nom du dossier
Anime_Name = "Chainsaw%20man"
# Anime_Name = "Beastars"
Sanitized_Anime_Name = Anime_Name.replace("%20", " ")  # Remplacer %20 par un espace pour le nom du dossier

# Utilitaire pour éviter les caractères illégaux dans les noms de fichiers/dossiers Windows
def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '', name)

# Télécharger une image dans un dossier spécifique avec une vérification de la validité de l'image
def downloadImg(url, imgName="", folder="") -> bool:
    if imgName == "":
        imgName = url.split("/")[-1]
    if folder != "":
        imgPath = os.path.join(folder, imgName)
    else:
        imgPath = os.path.join(OUTPUT_PATH, imgName)

    try:
        response = requests.get(url)

        # Vérifier si l'image existe (réponse 200 OK)
        if response.status_code != 200:
            print(f"Image non trouvée : {url}. Code HTTP : {response.status_code}")
            return False
        
        # Sauvegarder l'image si elle existe
        with open(imgPath, "wb") as handler:
            handler.write(response.content)
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image {url}: {e}")
        return False

# Créer un PDF à partir des images dans un dossier
def convertImgToPdf(image_files, output="output.pdf"):
    merger = PdfMerger()
    for image in image_files:
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(img2pdf.convert([image]))
                temp_file.flush()
            merger.append(temp_file.name)
        except Exception as e:
            print(f"Erreur lors de la création du PDF : {e}")
    merger.write(output)
    merger.close()

# Télécharger toutes les images d'un chapitre et les convertir en PDF
def downloadAndCreatePdf(chapter_number, Anime_Name, Sanitized_Anime_Name):
    # Créer un dossier principal pour le manga avec le nom de l'anime sans '%20'
    main_folder = os.path.join(OUTPUT_PATH, sanitize_filename(Sanitized_Anime_Name))
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
    
    # Liste pour stocker les chemins d'image pour le chapitre
    image_files = []
    
    page_number = 1
    while True:
        img_url = f"https://anime-sama.fr/s2/scans/{Anime_Name}/{chapter_number}/{page_number}.jpg"
        print(f"Téléchargement de l'image : {img_url}")
        
        # Télécharger l'image et ajouter son chemin à la liste
        img_name = f"{page_number}.jpg"
        if not downloadImg(img_url, imgName=img_name, folder=main_folder):
            print(f"Aucune image trouvée pour la page {page_number} du chapitre {chapter_number}. Arrêt du téléchargement.")
            break
        
        image_files.append(os.path.join(main_folder, img_name))
        page_number += 1
    
    # Créer le PDF une fois les images téléchargées
    pdf_output_path = os.path.join(main_folder, f"chapitre_{chapter_number}.pdf")
    convertImgToPdf(image_files, output=pdf_output_path)
    print(f"PDF créé pour le chapitre {chapter_number} à l'emplacement : {pdf_output_path}")
    
    # Supprimer les images après la création du PDF
    for img_file in os.listdir(main_folder):
        img_path = os.path.join(main_folder, img_file)
        if img_path.lower().endswith(('.png', '.jpeg', '.jpg')):
            os.remove(img_path)
            print(f"Image {img_file} supprimée.")
    
    print(f"Chapitre {chapter_number} téléchargé et converti en PDF avec succès.")

# Fonction pour télécharger un intervalle de chapitres
def downloadChaptersInRange(start_chapter, end_chapter, Anime_Name, Sanitized_Anime_Name):
    for chapter_number in range(start_chapter, end_chapter + 1):
        print(f"Téléchargement du chapitre {chapter_number}...")
        try:
            downloadAndCreatePdf(chapter_number, Anime_Name, Sanitized_Anime_Name)
        except Exception as e:
            print(f"Erreur lors du téléchargement du chapitre {chapter_number}: {e}")
            break

if __name__ == "__main__":
    start_chapter = int(input("Entrez le chapitre de début : "))
    end_chapter = int(input("Entrez le chapitre de fin : "))
    downloadChaptersInRange(start_chapter, end_chapter, Anime_Name, Sanitized_Anime_Name)
