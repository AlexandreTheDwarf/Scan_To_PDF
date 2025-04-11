import tkinter as tk
from tkinter import messagebox
import threading
import requests
import os
import re
from PyPDF2 import PdfMerger
import img2pdf
import tempfile

# Constantes
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output")

# Anime_Name avec '%20' pour l'URL, mais remplacement pour le nom du dossier
# Anime_Name = "Chainsaw%20man"
# Anime_Name = "Beastars"
# Anime_Name = "Solo%20Leveling"
# Anime_Name = "Demon%20Slayer"

# Utilitaire pour éviter les caractères illégaux dans les noms de fichiers/dossiers Windows
def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '', name)

def downloadImg(url, imgName="", folder="") -> bool:
    if imgName == "":
        imgName = url.split("/")[-1]
    if folder != "":
        imgPath = os.path.join(folder, imgName)
    else:
        imgPath = os.path.join(OUTPUT_PATH, imgName)

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Image non trouvée : {url}. Code HTTP : {response.status_code}")
            return False

        with open(imgPath, "wb") as handler:
            handler.write(response.content)
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image {url}: {e}")
        return False

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

def downloadAndCreatePdf(chapter_number, Anime_Name, Sanitized_Anime_Name, log_callback):
    main_folder = os.path.join(OUTPUT_PATH, sanitize_filename(Sanitized_Anime_Name))
    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    image_files = []
    page_number = 1
    while True:
        img_url = f"https://anime-sama.fr/s2/scans/{Anime_Name}/{chapter_number}/{page_number}.jpg"
        log_callback(f"Téléchargement de l'image : {img_url}")

        img_name = f"{page_number}.jpg"
        if not downloadImg(img_url, imgName=img_name, folder=main_folder):
            log_callback(f"Fin du chapitre {chapter_number} à la page {page_number - 1}")
            break

        image_files.append(os.path.join(main_folder, img_name))
        page_number += 1

    pdf_output_path = os.path.join(main_folder, f"chapitre_{chapter_number}.pdf")
    convertImgToPdf(image_files, output=pdf_output_path)
    log_callback(f"PDF créé : {pdf_output_path}")

    for img_file in os.listdir(main_folder):
        img_path = os.path.join(main_folder, img_file)
        if img_path.lower().endswith(('.png', '.jpeg', '.jpg')):
            os.remove(img_path)
    log_callback(f"Images supprimées pour le chapitre {chapter_number}")

def downloadChaptersInRange(start_chapter, end_chapter, Anime_Name, Sanitized_Anime_Name, log_callback):
    for chapter_number in range(start_chapter, end_chapter + 1):
        try:
            log_callback(f"\n--- Chapitre {chapter_number} ---")
            downloadAndCreatePdf(chapter_number, Anime_Name, Sanitized_Anime_Name, log_callback)
        except Exception as e:
            log_callback(f"Erreur lors du chapitre {chapter_number} : {e}")
            break

# Interface graphique
root = tk.Tk()
root.title("Manga Downloader GUI")
root.geometry("500x400")

def lancer_telechargement():
    anime = entry_anime.get().strip()
    if not anime:
        messagebox.showerror("Erreur", "Le nom de l'anime est requis.")
        return
    anime_url = anime.replace(" ", "%20")
    anime_clean = anime
    try:
        start = int(entry_start.get())
        end = int(entry_end.get())
        threading.Thread(target=downloadChaptersInRange, args=(start, end, anime_url, anime_clean, log)).start()
    except ValueError:
        messagebox.showerror("Erreur", "Les chapitres doivent être des nombres.")

def log(message):
    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nom de l'anime :").grid(row=0, column=0, sticky="e")
entry_anime = tk.Entry(frame, width=30)
entry_anime.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Chapitre de début :").grid(row=1, column=0, sticky="e")
entry_start = tk.Entry(frame, width=10)
entry_start.grid(row=1, column=1, sticky="w", pady=5)

tk.Label(frame, text="Chapitre de fin :").grid(row=2, column=0, sticky="e")
entry_end = tk.Entry(frame, width=10)
entry_end.grid(row=2, column=1, sticky="w", pady=5)

tk.Button(root, text="Télécharger", command=lancer_telechargement).pack(pady=10)

text_log = tk.Text(root, height=10, width=60)
text_log.pack(padx=10, pady=10)

root.mainloop()
