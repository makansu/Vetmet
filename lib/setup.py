import os
import subprocess
import sys
import platform

def run_command(command, critical=True):
    """Executes a system command, captures output, and handles errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✅ Success: {command}")
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        print(f"❌ Error ({command}): {error_message}")
        if critical:
            sys.exit(1)
        return False
    return True

def install_flutter():
    """Ensures Flutter is installed and updated with necessary dependencies."""
    print("Starting Flutter setup...")
    try:
        version_check = subprocess.run(["flutter", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if version_check.returncode != 0:
            print("❌ Flutter is not installed! Please install Flutter from https://flutter.dev/docs/get-started/install")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ Flutter command not found! Add it to your PATH.")
        sys.exit(1)

    run_command("flutter upgrade")
    run_command("flutter doctor")
    run_command("flutter pub get")
    print("✅ Flutter setup completed!")

def setup_android():
    """Configures Android SDK and builds APK."""
    print("Setting up Android environment...")
    android_home = os.environ.get("ANDROID_HOME")
    if not android_home:
        print("⚠️ Warning: ANDROID_HOME is not set! Ensure Android SDK is installed and environment variable is configured.")
    else:
        run_command(f"flutter config --android-sdk {android_home}")
    run_command("flutter build apk")
    print("✅ Android setup completed!")

def setup_ios():
    """Configures iOS dependencies and builds IPA."""
    if platform.system() != "Darwin":
        print("❌ iOS setup is only supported on macOS!")
        return
    if not os.path.isdir("ios"):
        print("❌ iOS directory missing! Ensure this is a valid Flutter project.")
        sys.exit(1)

    print("Setting up iOS environment...")
    run_command("cd ios && pod install")
    run_command("flutter build ios --release --no-codesign")
    print("✅ iOS setup completed!")

def create_codemagic_yaml():
    """Generates a Codemagic YAML file for automated CI/CD deployment."""
    print("Creating Codemagic configuration file...")

    yaml_content = """workflows:
  vetmet_app:
    name: Vetmet App CI/CD
    instance_type: mac_mini
    triggering:
      events:
        - push
        - pull_request
    environment:
      vars:
        ANDROID_HOME: $HOME/Library/Android/sdk
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
        print("✅ Codemagic YAML file created successfully.")
    except Exception as e:
        print(f"❌ Failed to create Codemagic YAML file: {e}")
        sys.exit(1)

def setup_firebase():
    """Installs Firebase CLI and authenticates user."""
    print("Setting up Firebase CLI...")
    run_command("npm install -g firebase-tools")
    run_command("firebase login")
    print("✅ Firebase setup completed!")

def main():
    print("==== Vetmet App Setup Script ====")
    install_flutter()
    setup_android()
    setup_ios()
    create_codemagic_yaml()
    setup_firebase()
    print("✅ All setup steps completed successfully!")

if __name__ == "__main__":
    main()