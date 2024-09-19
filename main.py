from utils.scanner import *
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
from fake_useragent import UserAgent
import time
import random
from utils.tray import *

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def User():
    ua = UserAgent()
    return ua.random

max_retries = 10

used_accs = []

def calis(retry_count=0,profile=None,action=None):
    global used_accs
    if retry_count >= max_retries:
        print(RED + "Maksimum yeniden deneme sayısına ulaşıldı. Program sonlandırılıyor." + RESET)
        sys.exit(1)
    if action == 1:
        base_profile_dir = os.path.join(os.getcwd(), "profiles", profile)

        # Edge tarayıcı ayarları
        options = Options()
        options.add_argument(f"user-data-dir={base_profile_dir}")  # Profil klasörünü belirt
        options.add_argument(f'user-agent={User()}')
        options.add_argument("--log-level=3")  # Konsol hatalarını sustur

        # WebDriver servisini otomatik yükleme ve başlatma
        service = Service(EdgeChromiumDriverManager().install())

        # Tarayıcıyı başlat
        driver = webdriver.Edge(service=service, options=options)

        # Belirtilen siteye git
        driver.get("https://www.algidailekazan.com/")
        asd = input("Giriş yaptıktan sonra enter'a basınız")
        sys.exit(1)
    try:
        hesaplar = ['emirhan', 'enes']
        hesap = random.choice(hesaplar)
        while hesap in used_accs:
            hesap = random.choice(hesaplar)
            time.sleep(1)
        used_accs.append(hesap)
            
        # Profilin saklanacağı klasörün yolu
        base_profile_dir = os.path.join(os.getcwd(), "profiles", hesap)

        # Edge tarayıcı ayarları
        options = Options()
        options.add_argument(f"user-data-dir={base_profile_dir}")  # Profil klasörünü belirt
        options.add_argument(f'user-agent={User()}')
        options.add_argument("--log-level=3")  # Konsol hatalarını sustur
        options.add_argument("--headless")

        # WebDriver servisini otomatik yükleme ve başlatma
        service = Service(EdgeChromiumDriverManager().install())

        # Tarayıcıyı başlat
        driver = webdriver.Edge(service=service, options=options)

        print(BLUE + f"{hesap} | Yetkilendirme anahtarı alınıyor..." + RESET)

        # Belirtilen siteye git
        driver.get("https://www.algidailekazan.com/")


        # Sayfa tamamen yüklendikten sonra bekleyelim (örneğin, 5 saniye bekleme)
        wait = WebDriverWait(driver, 10)
        try:
            point_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "homecodecard_pointField__QVqEf")))
            point_text = point_element.text.strip()
            print(f"{BLUE}{hesap.capitalize()} |{RESET}{GREEN} Güncel puan: {point_text}" + RESET)
        except:
            print(f"{hesap} | Oturumunuz sonlanmış, lütfen tekrar giriş yapınız.")
            calis(retry_count + 1)  # Yeniden başlatmayı çağır

        # Local Storage'dan istediğimiz değeri alalım
        script = """
        return window.localStorage.getItem('t');
        """
        local_storage_value = driver.execute_script(script)
        scripttwo = """
        return window.localStorage.getItem('c_i');
        """
        cid = driver.execute_script(scripttwo)

        if local_storage_value:
            print(GREEN + "Yetkilendirme anahtarı başarıyla alındı!" + RESET)
        else:
            print(RED + "Yetkilendirme anahtarı alınırken bir sorun oluştu!" + RESET)
        driver.quit()

        with open("kodlar.txt", "r") as file:
            kodlar = file.readlines()

        kodlar = [code.strip() for code in kodlar]

        for code in kodlar:
            print(code + " kodu deneniyor...")
            sonuc = kodugir(code, local_storage_value,cid)
            if sonuc == False:
                calis(retry_count + 1)  # Yeniden başlatmayı çağır
            time.sleep(5)
        print(RESET + GREEN + "Bütün kodlar denendi!" + RESET)
        sys.exit(1)

    except Exception as e:
        print(RED + f"Hata oluştu: {e}" + RESET)
        calis(retry_count + 1)  # Yeniden başlatmayı çağır

actions = int(input(f"1) {BLUE}Yeni hesap oluştur/giriş yap\n{RESET}2) {BLUE}Kapakları gir\n{RESET}3) {BLUE}Resimleri oku.\n{GREEN}Lütfen seçiminizi yapınız: " + RESET))
if actions == 1:
    isim = input("Profil ismi: ")
    calis(retry_count=0,profile=isim,action=actions)
elif actions == 2:
    calis(0,None,2)
elif actions == 3:
    while True:
        try:
            action = int(input(f"\n{RESET}1) {BLUE}Kopya resimleri temizle.\n{RESET}2) {BLUE}Kapakları oku.\n{RESET}3) {BLUE}Okunan kodlar\n{GREEN}Lütfen bir seçenek seçiniz: " + RESET))
        except ValueError:
            print("Lütfen geçerli bir sayı giriniz!")
            continue

        if action == 1:
            folder_path = 'kodlar'  # "kodlar" klasöründe çalışacak
            find_and_remove_duplicates(folder_path)
        elif action == 2:
            rename_and_move_files()
            break
        elif action == 3:
            folder = 'readed'
            print('\n')
            kodlistesi = []
            for filename in os.listdir(folder):
                try:
                    filename = filename.replace('.jpg', '').replace('.png','')
                except:
                    pass
                kodlistesi.append(filename)
                print(filename)
            sor = input("Kodlar kodlar.txt dosyasına taşınsın mı? (Y/N)   ")
            if sor.lower() == "y":
                with open("kodlar.txt", 'w') as file:
                    for code in kodlistesi:
                        file.write(code + '\n')
                
            break
        else:
            print("Lütfen geçerli bir seçenek seçiniz!")
