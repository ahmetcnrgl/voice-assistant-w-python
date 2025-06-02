import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import time
import sys

print("--- Asistan Uygulaması Başlatılıyor ---")

# Asistanın konuşma motorunu başlat
engine = None
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')


    found_turkish_voice = False
    for voice in voices:

        if "tr-TR" in voice.id.lower() or "turkish" in voice.name.lower() or "zira" in voice.name.lower() or "aylin" in voice.name.lower() or "asli" in voice.name.lower() or "cem" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            found_turkish_voice = True
            break

    if not found_turkish_voice:
        print("Uyarı: Türkçe ses bulunamadı. Varsayılan sistem sesi kullanılacak.")
        pass 

    engine.setProperty('rate', 180) 
    print("pyttsx3 konuşma motoru başarıyla başlatıldı.")
except Exception as e:
    print(f"Hata: pyttsx3 konuşma motoru başlatılırken bir sorun oluştu: {e}")
    print("Lütfen pyttsx3 ve ses paketlerinin doğru kurulduğundan emin olun.")
    print("Program sonlandırılıyor.")
    sys.exit(1)

def speak(text):
    """Asistanın metni sesli olarak okumasını ve konsola yazmasını sağlar."""
    if engine:
        print(f"Asistan: {text}")
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Hata: Sesli yanıt verilirken sorun oluştu (pyttsx3): {e}")
    else:
        print(f"Asistan (ses kapalı): {text}")

def listen_command():
    """Kullanıcının sesli komutunu dinler ve metne dönüştürür."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nDinliyorum...")
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Tanınıyor...")
            command = r.recognize_google(audio, language='tr-TR') 
            print(f"Sen: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Üzgünüm, ne dediğini anlayamadım.")
            speak("Üzgünüm, ne dediğinizi anlayamadım.")
            return ""
        except sr.RequestError as e:
            print(f"Hata: İnternet bağlantısı yok veya Google Speech API'ye erişilemiyor: {e}")
            speak("İnternet bağlantısı yok veya servis meşgul.")
            return ""
        except sr.WaitTimeoutError:
            print("Bir şey söylemediniz. Dinleme zaman aşımına uğradı.")
            speak("Bir şey söylemediğiniz için dinleme zaman aşımına uğradı.")
            return ""
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu (listen_command): {e}")
            speak(f"Beklenmeyen bir hata oluştu: {e}")
            return ""

def execute_command(command):
    """Alınan komutu işler ve uygun eylemi yapar."""
    print(f"Komut işleniyor: '{command}'")

    if "merhaba" in command:
        speak("Merhaba, size nasıl yardımcı olabilirim?")

    elif "saat kaç" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"Saat şu an {now}")

    elif "youtube'da aç" in command or "youtube'dan video aç" in command:
        speak("YouTube'da ne açmamı istersiniz?")
        query_text = listen_command()
        if query_text:
            speak(f"'{query_text}' YouTube'da açılıyor.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query_text}")
        else:
            speak("Video adı alamadım.")

    elif "kapan" in command or "çıkış" in command or "kapat" in command:
        speak("Görüşmek üzere!")
        return True

    else:
        speak("Üzgünüm, bu komutu anlayamadım.")

    return False

def main():
    """Ana uygulama döngüsü."""
    speak("Asistan başlatılıyor. Size nasıl yardımcı olabilirim?")
    while True:
        print("Komut dinleme döngüsü bekleniyor...")
        command = listen_command()
        if command:
            if execute_command(command):
                break
        time.sleep(0.5)

    print("Program sonlandırılıyor.")

if __name__ == "__main__":
    main()