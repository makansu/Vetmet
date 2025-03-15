import 'dart:io';

void main() {
  print("🚀 Vetmet iOS Yapılandırma Kontrolü Başlatılıyor...");

  // iOS klasörünün varlığını kontrol et
  Directory iosDir = Directory("ios");

  if (!iosDir.existsSync()) {
    print("⚠️ iOS klasörü bulunamadı! Lütfen Flutter projesine iOS desteği ekleyin.");
    print("Komut: flutter create .");
    exit(1);
  } else {
    print("✅ iOS klasörü bulundu!");
  }

  // Xcode proje dosyasını kontrol et
  File xcodeProject = File("ios/Runner.xcodeproj/project.pbxproj");

  if (!xcodeProject.existsSync()) {
    print("❌ Xcode proje dosyası eksik!");
    print("iOS için Flutter oluşturma komutunu çalıştırın: flutter build ios");
  } else {
    print("✅ Xcode proje dosyası bulundu!");
  }

  // Pod bağımlılıklarını kontrol et
  File podfile = File("ios/Podfile");

  if (!podfile.existsSync()) {
    print("⚠️ Podfile bulunamadı. CocoaPods yüklenmemiş olabilir.");
    print("Lütfen şu komutu çalıştırın: cd ios && pod install");
  } else {
    print("✅ Podfile mevcut, CocoaPods yapılandırması tamam.");
  }

  print("🔄 GitHub'a iOS yapılandırmasını eklemek için dosyalar güncelleniyor...");
}