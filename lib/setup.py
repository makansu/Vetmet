import os
import subprocess
import sys
import platform

def run_command(command):
    """Komutları çalıştır ve çıktıyı göster."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Başarılı: {command}")
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata ({command}): {e.stderr.strip()}")
        sys.exit(1)

def install_flutter():
    """Flutter SDK'nın güncellenmesini ve bağımlılıkların yüklenmesini sağlar."""
    print("🚀 Flutter kurulumu başlatılıyor...")
    
    # Flutter'ın sistemde olup olmadığını kontrol et
    try:
        run_command("flutter --version")
    except:
        print("❌ Flutter yüklü değil! Lütfen önce Flutter'ı yükleyin: https://flutter.dev/docs/get-started/install")
        sys.exit(1)

    run_command("flutter upgrade")
    run_command("flutter doctor")
    run_command("flutter pub get")
    print("✅ Flutter kurulumu tamamlandı!")

def setup_android():
    """Android ortamını hazırlar."""
    print("📱 Android ortamı kuruluyor...")
    
    # ANDROID_HOME kontrolü
    android_home = os.environ.get("ANDROID_HOME")
    if not android_home:
        print("⚠️ ANDROID_HOME tanımlanmamış! Android SDK'nın yüklü olduğundan emin olun.")
    
    run_command("flutter config --android-sdk $(echo $ANDROID_HOME)")
    run_command("flutter build apk")
    print("✅ Android kurulumu tamamlandı!")

def setup_ios():
    """iOS ortamını hazırlar."""
    if platform.system() != "Darwin":
        print("❌ iOS kurulumu yalnızca macOS sistemlerde desteklenir!")
        return

    if not os.path.isdir("ios"):
        print("❌ iOS klasörü bulunamadı! Flutter projesi değil mi?")
        sys.exit(1)
    
    print("🍏 iOS ortamı hazırlanıyor...")
    run_command("cd ios && pod install")
    run_command("flutter build ios --release --no-codesign")
    print("✅ iOS kurulumu tamamlandı!")

def create_codemagic_yaml():
    """Codemagic için YAML dosyasını oluşturur."""
    print("📄 Codemagic yapılandırma dosyası oluşturuluyor...")

    yaml_content = """\
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
    artifacts:
      - build/app/outputs/flutter-apk/app-release.apk
      - build/ios/ipa/*.ipa
"""

    try:
        with open("codemagic.yaml", "w") as f:
            f.write(yaml_content)
        print("✅ Codemagic YAML dosyası başarıyla oluşturuldu.")
    except Exception as e:
        print(f"❌ Codemagic YAML dosyası oluşturulamadı: {e}")
        sys.exit(1)

def main():
    install_flutter()
    setup_android()
    setup_ios()
    create_codemagic_yaml()
    print("🎉 Tüm kurulum başarıyla tamamlandı!")

if __name__ == "__main__":
    main()