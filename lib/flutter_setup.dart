import 'dart:io';

void main() async {
  print("🔄 Flutter SDK kurulumu başlatılıyor...");

  // Flutter SDK'nın kurulu olup olmadığını kontrol et
  var result = await Process.run('flutter', ['--version']);
  if (result.exitCode == 0) {
    print("✅ Flutter zaten yüklü: \n${result.stdout}");
  } else {
    print("❌ Flutter yüklü değil, şimdi yükleniyor...");

    // Flutter'ı indir ve yükle (Linux/macOS için)
    await installFlutter();
  }

  // PATH değişkenini güncelle
  await updatePath();

  // Flutter doktoru çalıştır
  await runFlutterDoctor();

  print("🚀 Flutter ortamı başarıyla hazırlandı!");
}

/// **Flutter SDK yükleme fonksiyonu**
Future<void> installFlutter() async {
  print("📥 Flutter indiriliyor...");

  var url = "https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.13.9-stable.tar.xz";
  var downloadCommand = "wget $url -O flutter.tar.xz";

  var extractCommand = "tar -xf flutter.tar.xz";
  var moveCommand = "mv flutter ~/flutter";

  await runCommand(downloadCommand);
  await runCommand(extractCommand);
  await runCommand(moveCommand);
  
  print("✅ Flutter başarıyla indirildi!");
}

/// **PATH değişkenini güncelleme fonksiyonu**
Future<void> updatePath() async {
  print("🔧 PATH değişkeni güncelleniyor...");

  var pathCommand = 'echo "export PATH=\$HOME/flutter/bin:\$PATH" >> ~/.bashrc';
  await runCommand(pathCommand);

  var reloadCommand = "source ~/.bashrc";
  await runCommand(reloadCommand);

  print("✅ PATH başarıyla güncellendi!");
}

/// **Flutter doktorunu çalıştırma fonksiyonu**
Future<void> runFlutterDoctor() async {
  print("🔎 Flutter doktoru çalıştırılıyor...");
  await runCommand("flutter doctor");
}

/// **Terminal komutlarını çalıştırma fonksiyonu**
Future<void> runCommand(String command) async {
  var result = await Process.run('bash', ['-c', command]);

  if (result.exitCode == 0) {
    print(result.stdout);
  } else {
    print("⚠️ Hata oluştu: ${result.stderr}");
  }
}