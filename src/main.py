import cv2 # Permissões da Webcam
import mediapipe as mp # <-- CORRIGIDO!
import random 
import os # <-- NOVO: Necessário para construir caminhos de arquivos

# --- NOVO: Define os caminhos dinamicamente ---
# Pega o caminho absoluto para o diretório onde este script está (src)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para o diretório raiz do projeto
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# -------------------------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --- FUNÇÃO ---
# Função para checar o "Joia" (Thumbs Up)
def is_thumbs_up(hand_landmarks):
    try:
        landmarks = hand_landmarks.landmark

        # Lógica para os 4 dedos fechados
        is_index_closed = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        is_middle_closed = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        is_ring_closed = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y
        is_pinky_closed = landmarks[mp_hands.HandLandmark.PINKY_TIP].y > landmarks[mp_hands.HandLandmark.PINKY_PIP].y
        
        # Lógica para o polegar aberto
        is_thumb_open = landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.THUMB_IP].y
        
        # Bônus: Para ser um "joia" clássico, o polegar deve estar acima do indicador
        is_thumb_above_index = landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y

        return is_index_closed and is_middle_closed and is_ring_closed and is_pinky_closed and is_thumb_open and is_thumb_above_index

    except Exception as e:
        return False

# --- UPLOAD DE IMAGEM (COM CAMINHO CORRIGIDO) ---

# !!! MUDE AQUI o nome da imagem (ela deve estar na pasta 'assets') !!!
IMAGE_FILENAME = 'joia.jpeg' 

# --- MUDANÇA IMPORTANTE AQUI ---
# Constrói o caminho completo para a imagem na pasta 'assets'
JOIA_IMAGE_PATH = os.path.join(PROJECT_ROOT, 'assets', IMAGE_FILENAME)
# ---------------------------------

# Definindo o tamanho da imagem
MEME_WIDTH = 200
MEME_HEIGHT = 150 

# Carregando a imagem que foi processada
loaded_joia_image = None

print(f"Carregando imagem: {JOIA_IMAGE_PATH}...")
try:
    img = cv2.imread(JOIA_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Não foi possível carregar: {JOIA_IMAGE_PATH}")
    
    # Redimensiona a imagem
    img_resized = cv2.resize(img, (MEME_WIDTH, MEME_HEIGHT), interpolation=cv2.INTER_AREA)

    # Processa a transparência (se for PNG)
    if img_resized.shape[2] == 4: 
        b, g, r, alpha = cv2.split(img_resized)
        img_bgr = cv2.merge((b, g, r))
        alpha_mask = alpha / 255.0
        loaded_joia_image = (img_bgr, alpha_mask) 
    else: # Se for JPG (sem transparência)
        loaded_joia_image = (img_resized, None) 
    
    print(f"Sucesso ao carregar e processar: {IMAGE_FILENAME}")

except Exception as e:
    print(f"--- ERRO FATAL ---")
    print(f"Não foi possível carregar a imagem: '{JOIA_IMAGE_PATH}'")
    print(f"Erro: {e}")
    print("Verifique o nome e se o arquivo existe na pasta 'assets'. O programa será fechado.")
    exit() # Encerra o script se a imagem não puder ser carregada

print(f"--- Imagem carregada. Iniciando webcam. ---")

# Inicializa a Webcam
cap = cv2.VideoCapture(0)

# Controle de estado
pose_detected_previously = False 

print("Mostre um sinal de 'Joia' (👍) para a câmera! Pressione 'q' para sair.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) # Inverte para modo selfie
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)

    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

    thumbs_up_count = 0
    pose_found_this_frame = False 

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                bgr_frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS)

            if is_thumbs_up(hand_landmarks):
                thumbs_up_count += 1
        
        if thumbs_up_count > 0:
            pose_found_this_frame = True
    
    # Configurando a exibição da imagem
    if pose_found_this_frame:
        if not pose_detected_previously:
            pose_detected_previously = True 
        
        img_bgr, img_alpha = loaded_joia_image
        
        # Posição da imagem (centralizada no topo)
        x_offset = int((bgr_frame.shape[1] - MEME_WIDTH) / 2)
        y_offset = 20 

        if y_offset + MEME_HEIGHT < bgr_frame.shape[0] and x_offset + MEME_WIDTH < bgr_frame.shape[1]:
            roi = bgr_frame[y_offset : y_offset + MEME_HEIGHT, x_offset : x_offset + MEME_WIDTH]

            if img_alpha is not None: 
                for c in range(0, 3):
                    bgr_frame[y_offset : y_offset + MEME_HEIGHT, x_offset : x_offset + MEME_WIDTH, c] = \
                        roi[:, :, c] * (1 - img_alpha) + \
                        img_bgr[:, :, c] * img_alpha
            else: 
                bgr_frame[y_offset : y_offset + MEME_HEIGHT, x_offset : x_offset + MEME_WIDTH] = img_bgr

    else: 
        pose_detected_previously = False

    cv2.imshow('Detector de Joia (Thumbs Up)', bgr_frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

print("Fechando...")
cap.release()
cv2.destroyAllWindows()
hands.close()