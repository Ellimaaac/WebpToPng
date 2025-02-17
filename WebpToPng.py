import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_webp_to_png(webp_path):
    try:
        root, file = os.path.split(webp_path)
        png_filename = os.path.splitext(file)[0] + ".png"
        png_path = os.path.join(root, png_filename)
        with Image.open(webp_path) as im:
            # Convertir en RGBA pour gérer la transparence, ou en RGB selon vos besoins
            im = im.convert("RGBA")
            im.save(png_path, "PNG")
        # Supprimer le fichier .webp après une conversion réussie
        os.remove(webp_path)
        return f"Converti et supprimé : {webp_path} -> {png_path}"
    except Exception as e:
        return f"Erreur lors de la conversion de {webp_path} : {e}"

def main():
    parent_dir = r"your_path_folder"  # Adaptez ce chemin
    webp_files = []

    # Parcourir récursivement tous les sous-dossiers pour collecter les fichiers .webp
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.lower().endswith(".webp"):
                webp_files.append(os.path.join(root, file))

    # Utiliser un ThreadPoolExecutor pour traiter plusieurs fichiers en parallèle
    with ThreadPoolExecutor(max_workers=14) as executor:
        futures = [executor.submit(convert_webp_to_png, webp) for webp in webp_files]
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    main()
