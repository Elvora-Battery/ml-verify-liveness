import cv2
import requests

# URL API Flask
url = 'http://127.0.0.1:5000/detect_liveness'

# Menginisialisasi kamera (webcam)
cap = cv2.VideoCapture(0)

# Status verifikasi
smile_verified = False
tilt_verified = False

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()
    
    # Konversi frame ke format yang bisa dikirim
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': img_encoded.tobytes()}
    
    # Kirim frame ke API Flask untuk deteksi liveness
    response = requests.post(url, files=files)
    result = response.json()

    # Langkah pertama: Instruksi untuk tersenyum
    if not smile_verified:
        cv2.putText(frame, "Silakan tersenyum", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        if result:
            for face_data in result:
                smile_detected = face_data['smile_detected']

                # Jika senyuman terdeteksi, lanjutkan ke tahap selanjutnya
                if smile_detected:
                    smile_verified = True

    # Langkah kedua: Instruksi untuk memiringkan kepala
    elif not tilt_verified:
        cv2.putText(frame, "Miringkan kepala ke kanan/kiri", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        if result:
            for face_data in result:
                head_tilt_angle = face_data['head_tilt_angle']

                # Jika kemiringan kepala terdeteksi (misal lebih dari 10 derajat)
                if abs(head_tilt_angle) > 10:
                    tilt_verified = True

    # Jika kedua langkah berhasil, tampilkan verifikasi berhasil
    if smile_verified and tilt_verified:
        cv2.putText(frame, "Verify berhasil", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Tampilkan frame video dengan instruksi
    cv2.imshow('Live Video', frame)

    # Tekan 'q' untuk keluar dari video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan sumber daya
cap.release()
cv2.destroyAllWindows()
