#!/usr/bin/env bash
# Wrap a finished PWA folder into an Android APK with Capacitor, for the user's own phone only.
# Never upload the result to Google Play or any public page.
# Tested 2026-10-30 on the template scaffold: Capacitor 8.6.0 (MIT), Node 22.23.4, Temurin JDK 21.0.13,
# Android cmdline-tools 13114758 / platform 36 / build-tools 36.0.0. Re-check versions before use.
#
# Usage: make_apk.sh <app-dir> <package-id> "<App Name>" <work-dir> <keystore-path>
#   e.g. make_apk.sh apps/pocket-puzzles app.example.pocketpuzzles "Pocket Puzzles" /tmp/apk-build private/pocket-puzzles-keys/release.keystore
# Needs: TOOLS dir with node22, jdk21 and the Android SDK (see the "setup" block below).
# The keystore password is read from KS_PASS. It's generated once per app and stored with the vault rules, never in a file in apps/.
set -euo pipefail
APP_DIR=$(realpath "$1"); PKG="$2"; NAME="$3"; WORK="$4"; KS=$(realpath -m "$5")
TOOLS=${TOOLS:-/tmp/apk}
: "${KS_PASS:?set KS_PASS}"

# --- setup (once; no root needed) ---
# cd $TOOLS
# curl -sL -o jdk.tgz "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jdk/hotspot/normal/eclipse" && tar xzf jdk.tgz
# curl -sL -o node.txz https://nodejs.org/dist/latest-v22.x/node-v22.<x>-linux-x64.tar.xz && tar xJf node.txz
# curl -sL -o clt.zip https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip && unzip -q clt.zip
# mkdir -p sdk/cmdline-tools && mv cmdline-tools sdk/cmdline-tools/latest
# sdk/cmdline-tools/latest/bin/sdkmanager --licenses   # read and accept the Android SDK license
# sdk/cmdline-tools/latest/bin/sdkmanager "platforms;android-36" "build-tools;36.0.0" "platform-tools"

export JAVA_HOME=$(ls -d $TOOLS/jdk-21*) ANDROID_HOME=$TOOLS/sdk
export PATH=$(ls -d $TOOLS/node-v22*)/bin:$JAVA_HOME/bin:$PATH
BT=$ANDROID_HOME/build-tools/36.0.0

mkdir -p "$WORK/www" && cd "$WORK"
rm -rf www && mkdir www && cp -r "$APP_DIR"/. www/ && rm -f www/README.md www/NOTES.md www/research.md
[ -f package.json ] || npm init -y >/dev/null
npm i --silent @capacitor/core@8 @capacitor/android@8 && npm i --silent -D @capacitor/cli@8
[ -f capacitor.config.json ] || npx cap init "$NAME" "$PKG" --web-dir www
[ -d android ] || npx cap add android
npx cap sync android
echo "sdk.dir=$ANDROID_HOME" > android/local.properties

if [ ! -f "$KS" ]; then
  mkdir -p "$(dirname "$KS")"
  keytool -genkeypair -keystore "$KS" -alias app -keyalg RSA -keysize 4096 -validity 10000 \
    -storepass "$KS_PASS" -keypass "$KS_PASS" -dname "CN=Personal" >/dev/null
  echo "NEW KEY: $KS. Back it up; every update must use this key."
fi

(cd android && ./gradlew assembleRelease --no-daemon -q)
"$BT/zipalign" -f -p 4 android/app/build/outputs/apk/release/app-release-unsigned.apk aligned.apk
"$BT/apksigner" sign --ks "$KS" --ks-key-alias app --ks-pass env:KS_PASS --out "$NAME.apk" aligned.apk
"$BT/apksigner" verify --print-certs "$NAME.apk" | head -2
"$BT/aapt2" dump badging "$NAME.apk" | head -1
echo "APK: $WORK/$NAME.apk"
