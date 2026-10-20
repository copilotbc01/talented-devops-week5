# Talented DevOps - Hafta 5

**Binnur Cerit | 20 Ekim 2026**

Cloud Operations / Platform & Cloud Engineering patikasında, önceki Terraform
laboratuvarımı CI kalite kontrollerine bağladım. Python servisi için çok aşamalı
Docker build, güvenlik kapısı ve sürümlü GHCR yayını oluşturdum.

## Doğrulanmış sonuçlar

- [Başarılı v1.0.0 çalıştırması](https://github.com/copilotbc01/talented-devops-week5/actions/runs/39465329218)
- [Kasıtlı başarısız test dalı](https://github.com/copilotbc01/talented-devops-week5/actions/runs/39464344732)
- [Debian imajında gerçek CVE engeli](https://github.com/copilotbc01/talented-devops-week5/actions/runs/39464774284)
- [GHCR paket ve etiket ekranı](https://github.com/copilotbc01/talented-devops-week5/pkgs/container/talented-devops-week5)

Python 3.11 ve 3.12 üzerinde Flake8 ve 11 birim testi başarılıdır.
Terraform fmt/init/validate ve gerçek container health kontrolü başarılıdır.
İlk Debian imajındaki 44 HIGH paket-bulgu kaydı nedeniyle yayın engellendi.
Alpine tabanına geçildikten sonra aynı güvenlik eşiğinde HIGH/CRITICAL bulunmadı.
Tarama sonucu yalnızca çalıştırma anındaki veri tabanı ve belirtilen eşik içindir.

## Yerel tekrar

```sh
python -m pip install flake8==7.1.2
python -m flake8 .
python -m unittest discover -s tests -v
python ops.py
python ops.py gate fixtures/clean.json
python ops.py gate fixtures/high.json
```

Son komutun çıkış kodunun 1 olması beklenir: yapay HIGH girdisini engeller.
`ops.py` rollback kararını bellek içinde simüle eder; gerçek sunucuya dağıtım yapmaz.

```sh
docker build -t talented-week5 .
docker run --rm -p 127.0.0.1:8080:8080 talented-week5
# Ayrı terminal:
curl --fail http://127.0.0.1:8080/health
```

## İş akışı

Her push/PR: Python matrix kalite ve testleri, Terraform doğrulama,
Docker build, container smoke testi ve gerçek Trivy taraması.
HIGH/CRITICAL bulgular (düzeltmesi henüz olmayanlar dahil) yayın kapısını kapatır.
PR ve dal push'larında registry login/push çalışmaz.

Kararlı `vMAJOR.MINOR.PATCH` tag push'u bütün kontrolleri tekrar çalıştırır;
sonra aynı taranmış imajı sürüm ve commit etiketleriyle GHCR'a gönderir.
İlk sürüm `v1.0.0` zaten yayımlanmıştır. Yeni sürüm için yeni etiket kullanılmalıdır.
Ön sürüm/build metadata tag biçimleri bu uygulamada desteklenmez.

## Güvenlik ve sınırlar

- Token yalnızca registry login girdisinde kullanılır; Docker ARG/ENV içine yazılmaz.
- PR'da registry login/push yoktur; pull_request_target kullanılmaz.
- Uygulama root olmayan UID 10001 ile çalışır.
- Trivy action referansı doğrulanmış commit SHA'ya sabittir. Diğer action tag'leri ve
  base image etiketi canlı kullanımda ayrıca onaylı SHA/digest ile sabitlenmelidir.
- packages:write yalnızca imaj job'unda tanımlıdır.
- Bu iş akışı imaj yayımlar; üretim sunucusuna deployment yapmaz.
- Rollback bir karar modeli olarak test edilmiştir.
- previous-week4/terraform önceki kaynakları içerir. Yeni pipeline Terraform apply
  veya LocalStack entegrasyonu çalıştırmaz.

Teknik teslim ZIP'inde PDF, tarihli ekran görüntüleri, tam CI logları,
Trivy JSON raporları ve SHA256 manifesti bulunur. Geçmiş hafta kanıtları
previous-week4/evidence altında ayrı tutulur; yeni haftanın kanıtı olarak sunulmaz.
