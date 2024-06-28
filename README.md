# Algida ile Kazan Otomasyon Uygulaması

Bu Python uygulaması, kullanıcıların "Algida ile Kazan" uygulamasına kendi hesaplarıyla giriş yapmalarını, oturumlarını kaydetmelerini ve Algida dondurma kutusu kodları bulunan resimlerdeki kodları okuyarak otomatik olarak bu kodları girmelerini sağlar. Kodlar, "Kullanılmış", "Başarılı" ve "Hatalı kod" şeklinde gruplara ayrılır.

## Özellikler

- Kullanıcı oturum açma ve oturum kaydetme
- Resimlerdeki kodları otomatik olarak okuma
- Kodları hesaplara girme
- Kodları başarı durumlarına göre sınıflandırma (Kullanılmış, Başarılı, Hatalı kod)

## Gereksinimler

- Python 3.x
- Aşağıdaki Python kütüphaneleri:
  - `requests`
  - `beautifulsoup4`
  - `opencv-python`
  - `pytesseract`

## Kurulum

1. Bu repository'yi klonlayın:
    ```bash
    git clone https://github.com/3miRuna/Kapak-okuyucu
    cd Kapak-okuyucu
    ```

2. Gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

Hazırlık: Görsellerinizi "Kodlar" klasörüne kopyalayın.

1. Uygulamayı çalıştırmak için aşağıdaki komutu kullanın:
    ```bash
    python main.py
    ```

2. Uygulama, belirtilen resim dosyalarındaki kodları okuyacak ve giriş yaptığınız hesaplarda bu kodları kullanacaktır.

3. Kodların durumu, sonuç dosyasında "Kullanılmış", "Başarılı" ve "Hatalı kod" olarak listelenecektir.

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir fork oluşturun ve değişikliklerinizi bir pull request ile gönderin. Her türlü katkı değerlidir ve memnuniyetle kabul edilir.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

---

Bu uygulamayı kullanarak Algida ile Kazan deneyiminizi daha verimli hale getirin!
