import os
from google.cloud import vision
import hashlib

def hash_file(file_path):
    """Dosyanın hash değerini hesaplar."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_and_remove_duplicates(folder_path):
    """Klasördeki aynı .png ve .jpg dosyalarını bulur ve bir tanesini siler."""
    duplicatesayisi = 0
    hashes = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                file_path = os.path.join(root, file)
                file_hash = hash_file(file_path)
                if file_hash in hashes:
                    duplicatesayisi += 1
                    os.remove(file_path)
                else:
                    hashes[file_hash] = file_path
    print(f"{duplicatesayisi} adet tekrar eden görsel bulundu ve silindi!")

def rename_and_move_files():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cred.json'
    client = vision.ImageAnnotatorClient()

    results = []

    readed_folder = 'readed'
    if not os.path.exists(readed_folder):
        os.makedirs(readed_folder)
    
    couldnt_read_folder = 'couldntreaded'
    if not os.path.exists(couldnt_read_folder):
        os.makedirs(couldnt_read_folder)

    kodlar_folder = 'kodlar'
    image_files = [file for file in os.listdir(kodlar_folder) if file.endswith('.jpg') or file.endswith('.png')]
    for filename in image_files:
        file_path = os.path.join(kodlar_folder, filename)
        with open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            unique_texts = set()
            for text in texts:
                if ' ' not in text.description and 8 <= len(text.description) <= 12:
                    if text.description not in unique_texts:
                        unique_texts.add(text.description)
                        new_filename = f'{text.description}.jpg'
                        new_filepath = os.path.join(readed_folder, new_filename)

                        if os.path.exists(new_filepath):
                            base, extension = os.path.splitext(new_filename)
                            counter = 1
                            while os.path.exists(new_filepath):
                                new_filename = f'{base}_{counter}{extension}'
                                new_filepath = os.path.join(readed_folder, new_filename)
                                counter += 1

                        try:
                            os.rename(file_path, new_filepath)
                            print(f'{filename} | {text.description}')
                        except FileNotFoundError:
                            print(f"Hata: {file_path} dosyası taşınamadı.")
                        results.append(text.description)
        else:
            couldnt_read_path = os.path.join(couldnt_read_folder, filename)
            os.rename(file_path, couldnt_read_path)
            print(f'{filename} | Metin bulunamadı.')

    print("\nToplu olarak kodlar:\n")
    for result in results:
        print(result)
