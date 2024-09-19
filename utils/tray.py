import requests

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def kodugir(code, token,cid):
    url = "https://prodapi-kazan.algida.me/electra/api/promo/checkStickcode"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://www.algidailekazan.com",
        "Referer": "https://www.algidailekazan.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    data = {
        "CustomerID": cid,
        "StickCode": code,
        "appKey": "830DA10A-FA97-4244-8B40-E97EC8F085D9"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # HTTP hata durumlarını kontrol et
        json_response = response.json()
        if isinstance(json_response, list) and len(json_response) > 0:
            Message = json_response[0].get('Message', 'Message bulunamadı')
            Title = json_response[0].get('Title', 'Title bulunamadı')

            

            if Title == "Kod giriş limitine ulaştınız!":
                print(RED + "Günlük limitiniz doldu!" + RESET)
                return False
            elif Message == "Lütfen kodu doğru girdiğinizden emin olunuz.":
                print(BLUE + code + RESET + RED + " | Hatalı kod! Lütfen kodu kontrol ediniz." + RESET)
                remove_code_from_file(code, "kodlar.txt", "hatalikod.txt")
            elif Message == "Kısa süre içerisinde çok fazla deneme yaptınız, lütfen daha sonra tekrar deneyiniz.":
                print(BLUE + code + RESET + RED + " | Çok fazla deneme yaptınız, lütfen daha sonra tekrar deneyiniz." + RESET)
                print(BLUE + "Hesap değiştiriliyor..." + RESET)
                return False
            elif Message == "Kod daha önce kullanılmıştır, lütfen farklı bir kod ile tekrar deneyiniz":
                print(RED + code + " | Kod daha önce kullanılmış!" + RESET)
                remove_code_from_file(code, "kodlar.txt", "kullanilmis.txt")
            elif Message == "Hediyenizi daha önce aldınız. Çekilişe katılabilirsiniz!":
                print(GREEN + Message + RESET)
                remove_code_from_file(code, "kodlar.txt", "zatenkullandin.txt")
            else:
                for item in json_response:
                    if 'Point' in item:
                        print(BLUE + f"{code} | Koddan çıkan puan:" + RESET + GREEN + f" {item['Point']}" + RESET)
                        remove_code_from_file(code, "kodlar.txt", "success.txt")
                print(json_response)
        else:
            print("Response formatı beklenildiği gibi değil.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def remove_code_from_file(code, source_file, destination_file):
    try:
        with open(source_file, 'r') as file:
            lines = file.readlines()
        with open(source_file, 'w') as file:
            for line in lines:
                if line.strip("\n") != code:
                    file.write(line)
        with open(destination_file, 'a') as file:
            file.write(code + "\n")
    except Exception as e:
        print("Dosya işlemi sırasında hata:", e)
