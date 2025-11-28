import cv2
import numpy as np

def computeArea(img):
    # 1. Converter para Escala de Cinza (Padrão)
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # 2. Suavização (Blur)
    # Essencial para o Canny não detectar ruído como borda
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # 3. Detecção de Bordas (Canny)
    # Detecta mudanças bruscas de intensidade
    edges = cv2.Canny(blurred, 30, 30)

    # 4. Contagem
    n_pixels = np.sum(edges == 255)

    return n_pixels, edges