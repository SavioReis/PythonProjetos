import cv2

# Carrega os classificadores para detecção de faces e sorrisos
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smileCascade = cv2.CascadeClassifier('haarcascade_smile.xml')

# Carrega as imagens dos emojis
emoji_happy = cv2.imread('emoji_happy.png', cv2.IMREAD_UNCHANGED)
emoji_sad = cv2.imread('emoji_sad.png', cv2.IMREAD_UNCHANGED)
emoji_neutral = cv2.imread('emoji_neutral.png', cv2.IMREAD_UNCHANGED)

# Define a escala para redimensionar os emojis
emoji_scale = 0.2

# Redimensiona os emojis
emoji_happy_resized = cv2.resize(emoji_happy, (0, 0), fx=emoji_scale, fy=emoji_scale)
emoji_sad_resized = cv2.resize(emoji_sad, (0, 0), fx=emoji_scale, fy=emoji_scale)
emoji_neutral_resized = cv2.resize(emoji_neutral, (0, 0), fx=emoji_scale, fy=emoji_scale)

# Inicia a captura de vídeo da câmera
capture = cv2.VideoCapture(0)

while True:
    # Captura o frame da câmera
    ret, frame = capture.read()

    # Converte o frame para escala de cinza
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta as faces no frame
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Para cada face detectada, verifica se há um sorriso
    for (x, y, w, h) in faces:
        faceROI_gray = gray[y:y + h, x:x + w]
        faceROI_color = frame[y:y + h, x:x + w]

        smiles = smileCascade.detectMultiScale(faceROI_gray, scaleFactor=1.7, minNeighbors=22, minSize=(25, 25))

        # Exibe um retângulo ao redor da face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Verifica a presença de sorriso e exibe o emoji correspondente
        if len(smiles) > 0:
            emoji_x = x + int(w/2) - int(emoji_happy_resized.shape[1]/2)  # Centraliza o emoji no eixo x
            emoji_y = y - emoji_happy_resized.shape[0]  # Posição do emoji no topo da face

            # Verifica se a região do emoji está dentro dos limites do frame
            if emoji_y >= 0 and emoji_x >= 0 and emoji_x + emoji_happy_resized.shape[1] <= frame.shape[1]:
                # Mescla o emoji com o frame, considerando a transparência
                alpha_mask = emoji_happy_resized[:, :, 3] / 255.0
                alpha_inv_mask = 1.0 - alpha_mask

                for c in range(3):
                    frame_roi = frame[emoji_y:emoji_y + emoji_happy_resized.shape[0], emoji_x:emoji_x + emoji_happy_resized.shape[1], c]
                    emoji_roi = emoji_happy_resized[:, :, c] * alpha_mask + frame_roi * alpha_inv_mask
                    frame[emoji_y:emoji_y + emoji_happy_resized.shape[0], emoji_x:emoji_x + emoji_happy_resized.shape[1], c] = emoji_roi

        else:
            emoji_x = x + int(w/2) - int(emoji_neutral_resized.shape[1]/2)  # Centraliza o emoji no eixo x
            emoji_y = y - emoji_neutral_resized.shape[0]  # Posição do emoji no topo da face

            # Verifica se a região do emoji está dentro dos limites do frame
            if emoji_y >= 0 and emoji_x >= 0 and emoji_x + emoji_neutral_resized.shape[1] <= frame.shape[1]:
                # Mescla o emoji com o frame, considerando a transparência
                alpha_mask = emoji_neutral_resized[:, :, 3] / 255.0
                alpha_inv_mask = 1.0 - alpha_mask

                for c in range(3):
                    frame_roi = frame[emoji_y:emoji_y + emoji_neutral_resized.shape[0], emoji_x:emoji_x + emoji_neutral_resized.shape[1], c]
                    emoji_roi = emoji_neutral_resized[:, :, c] * alpha_mask + frame_roi * alpha_inv_mask
                    frame[emoji_y:emoji_y + emoji_neutral_resized.shape[0], emoji_x:emoji_x + emoji_neutral_resized.shape[1], c] = emoji_roi

    # Exibe o frame resultante
    cv2.imshow('Emotion Recognition', frame)

    # Verifica se a tecla 'q' foi pressionada para encerrar o programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
capture.release()
cv2.destroyAllWindows()
