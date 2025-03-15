import os
import subprocess
import sys

def run_command(command):
    """Komutları çalıştır ve çıktı ver."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Başarılı: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata: {e.stderr.strip()}")
        sys.exit(1)

def install_flutter():
    """Flutter SDK'nın güncellenmesini ve bağımlılıkların yüklenmesini sağlar."""
    print("🚀 Flutter kurulumu başlatılıyor...")
    run_command("flutter upgrade")
    run_command("flutter doctor")
    run_command("flutter pub get")
    print("✅ Flutter kurulumu tamamlandı!")

def setup_android():
    """Android ortamını hazırlar."""
    print("📱 Android ortamı kuruluyor...")
    run_command("flutter config --android-sdk $(echo $ANDROID_HOME)")
    run_command("flutter build apk")
    print("✅ Android kurulumu tamamlandı!")

def setup_ios():
    """iOS ortamını hazırlar."""
    if not os.path.isdir("ios"):
        print("❌ iOS klasörü bulunamadı! Flutter projesi değil mi?")
        sys.exit(1)
    
    print("🍏 iOS ortamı hazırlanıyor...")
    run_command("cd ios && pod install")
    print("✅ iOS kurulumu tamamlandı!")

def create_codemagic_yaml():
    """Codemagic için YAML dosyasını oluşturur."""
    yaml_content = """
workflows:
  vetmet_app:
    name: Vetmet App CI/CD
    instance_type: mac_mini
    triggering:
      events:
        - push
        - pull_request
    scripts:
      - flutter pub get
      - flutter build apk
      - flutter build ios --release --no-codesign
"""
    with open("codemagic.yaml", "w") as f:
        f.write(yaml_content)
    print("✅ Codemagic YAML dosyası oluşturuldu.")

def main():
    install_flutter()
    setup_android()
    setup_ios()
    create_codemagic_yaml()
    print("🎉 Tüm kurulum başarıyla tamamlandı!")

if __name__ == "__main__":
    main()