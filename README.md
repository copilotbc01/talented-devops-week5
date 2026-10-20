# Talented DevOps - Hafta 5

Ana patika: Platform & Cloud Engineering. Ek: SRE güvenlik kapısı ve rollback modeli.
Bu paket yerel test edilmiş bir uygulama ve CI/CD tasarımıdır. Canlı GitHub Actions,
GHCR, Docker/Trivy ve sertifikasyon modülü tamamlanmış gibi sunulmamıştır.

## Yerel kullanım

Python 3.11 veya 3.12:

```sh
python -m unittest discover -s tests -v
python ops.py
python ops.py gate fixtures/clean.json
python ops.py gate fixtures/high.json  # Beklenen çıkış kodu: 1
python app.py
# Ayrı terminal:
curl http://localhost:8080/health
```

Kalite denetimi:

```sh
python -m pip install flake8==7.1.2
python -m flake8 .
```

## GitHub ve GHCR

1. Bu klasörün içeriğini kendi GitHub depona ekle; .github klasörünü de yükle.
2. Actions çalıştırmalarına izin ver. Paket oluşturma kurum politikasınca engelleniyorsa
   yöneticinle görüş. GITHUB_TOKEN otomatik oluşturulur; ayrıca token dosyası ekleme.
3. Push/PR: iki Python sürümünde lint/test, imaj derleme, smoke test ve Trivy taraması.
4. Başarılı kontrollerden sonra sürüm oluştur:

```sh
git tag v1.0.0
git push origin v1.0.0
```

5. Etiket push'u bütün kontrolleri tekrar çalıştırır; yalnızca HIGH/CRITICAL yoksa,
   taranmış imajı ghcr.io/OWNER/REPO:1.0.0 ve :sha-COMMIT etiketleriyle yayımlar.
   OWNER/REPO workflow içinde küçük harfe dönüştürülür. Desteklenen sürümler
   kararlı vMAJOR.MINOR.PATCH biçimindedir; ön sürüm etiketleri bilerek reddedilir.
6. Actions logları, Trivy artifact'i ve GHCR etiket ekranını kanıt olarak kaydet.

## Kasıtlı başarısız CI kanıtı

Ayrı bir test dalında tests/test_app.py içindeki health beklentisini yanlış değiştirip
PR aç. Test job'u kırılmalı; build-scan-publish atlanmalı. Log ekranını kaydet,
sonra değişikliği geri al. Ana dala bilerek bozuk test birleştirme.
Fixture HIGH testi beklenen hata kodunu doğruladığı için ana workflow'u kırmaz.
Gerçek CVE halinde Trivy adımı workflow'u kırar ve publish çalışmaz.

## Güvenlik ve kapsam

- PR'da registry login/push yok; pull_request_target kullanılmaz.
- Çalıştırılabilir shell metnine doğrudan PR başlığı/ref ifadesi gömülmez.
- Token yalnızca login adımına verilir; Docker ARG/ENV veya log içine yazılmaz.
- Runtime root olmayan UID 10001 kullanır; test dosyaları final imaja girmez.
- Bağımlılıksız uygulama için multi-stage boyut kazancı sınırlıdır.
- Base image etiketi hareketlidir; canlı kullanımda onaylı digest sabitlenmeli.
- Action sürümleri etiketlidir; canlı kullanımda doğrulanmış commit SHA ile sabitlenmeli.
- packages:write build job'una verilmiştir; daha sıkı yalıtım için yayımlama ayrı,
  korumalı environment ve onay kapısıyla yapılabilir.
- Bu iş akışı konteyner yayımlar; üretim sunucusuna dağıtım yapmaz.
- ops.py gerçek Docker rollback'i değildir: sağlık başarısızlığında önceki sürüme
  dönüş kararını ve rollback hatasında eskalasyonu test eden bellek içi modeldir.

## Göndermeden önce kalan kişisel kanıtlar

PDF ve ZIP dosya adları önceki teslimlerdeki BinnurCerit adına göre belirlenmiştir.
Hafta 3'te seçtiğin gerçek sertifikasyon patikasının modül 3 ekran görüntülerini,
lab sonuçlarını ve gerçek ilerleme oranını ekle. Paketteki AWS özeti örnek çalışma
notudur; bir kursu tamamladığını veya bir sınavı geçtiğini kanıtlamaz.

## Önceki çalışmalarla devamlılık
Hafta 3/4 Platform & Cloud Engineering seçimi ve AWS Solutions Architect - Associate
çalışma hedefi korunmuştur. previous-week4 klasörü önceki arşivden alınan Terraform
kaynaklarını ve açıkça tarihlenmiş geçmiş kanıtları içerir. CI bu kaynaklara fmt/init/validate
uygular; Terraform apply ve LocalStack entegrasyonu bu yeni workflow içinde çalıştırılmaz.

## Önceki çalışmalarla devamlılık
Hafta 3/4 Platform & Cloud Engineering seçimi ve AWS Solutions Architect - Associate
çalışma hedefi korunmuştur. previous-week4 klasörü önceki arşivden alınan Terraform
kaynaklarını ve açıkça tarihlenmiş geçmiş kanıtları içerir. CI bu kaynaklara fmt/init/validate
uygular; Terraform apply ve LocalStack entegrasyonu bu yeni workflow içinde çalıştırılmaz.
