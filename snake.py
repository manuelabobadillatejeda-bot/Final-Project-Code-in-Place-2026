import pygame
import random
import sys

pygame.init()


TAMANO_PANTALLA = 750
TAMANO_BLOQUE = 40
CUADRICULA = TAMANO_PANTALLA // TAMANO_BLOQUE


COLOR_FONDO = (26, 26, 26)       # Gris oscuro
COLOR_SERPIENTE = (76, 175, 80)   # Verde principal
COLOR_MANZANA = (255, 71, 87)     # Rojo manzana
COLOR_TEXTO = (255, 255, 255)     # Blanco
COLOR_TEXTO_2 = (143, 143, 143)      # Gris claro


pantalla = pygame.display.set_mode((TAMANO_PANTALLA, TAMANO_PANTALLA))
pygame.display.set_caption("Juego de la Serpiente")
reloj = pygame.time.Clock()

# --- CARGA SEGURA DE SONIDOS ---
sonido_comer = None
sonido_game_over = None

sonido_comer = pygame.mixer.Sound("Sounds/eat.mp3")
sonido_game_over = pygame.mixer.Sound("Sounds/wall.mp3")



def pantalla_inicio():
    fuente_titulo = pygame.font.SysFont("gothambold", 60, bold=True)
    fuente_sub = pygame.font.SysFont("gothamlight", 38)
    
    texto_titulo = fuente_titulo.render("SNAKE GAME", True, COLOR_SERPIENTE)
    texto_instrucciones = fuente_sub.render("Press the SPACE key to start", True, COLOR_TEXTO)
    texto_controles = fuente_sub.render("Use the arrows to move", True, (150, 150, 150))
    
    while True:
        pantalla.fill(COLOR_FONDO)
        
        pantalla.blit(texto_titulo, (TAMANO_PANTALLA // 2 - texto_titulo.get_width() // 2, TAMANO_PANTALLA // 3))
        pantalla.blit(texto_instrucciones, (TAMANO_PANTALLA // 2 - texto_instrucciones.get_width() // 2, TAMANO_PANTALLA // 2))
        pantalla.blit(texto_controles, (TAMANO_PANTALLA // 2 - texto_controles.get_width() // 2, TAMANO_PANTALLA // 2 + 40))
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return 

def dibujar_manzana(x, y):
    centro_x = x * TAMANO_BLOQUE + TAMANO_BLOQUE // 2
    centro_y = y * TAMANO_BLOQUE + TAMANO_BLOQUE // 2
    radio = TAMANO_BLOQUE // 2 - 2
    
    # 1. Cuerpo de la manzana (Círculo rojo)
    pygame.draw.circle(pantalla, COLOR_MANZANA, (centro_x, centro_y), radio)
    # Brillo para dar efecto 3D
    pygame.draw.circle(pantalla, (255, 120, 130), (centro_x - 3, centro_y - 3), 3)
    
    # 2. Tallo (Línea café)
    pygame.draw.line(pantalla, (139, 69, 19), (centro_x, centro_y - radio), (centro_x + 3, centro_y - radio - 4), 2)
    
    # 3. Hoja (Pequeño triángulo verde)
    pygame.draw.polygon(pantalla, (50, 205, 50), [
        (centro_x + 2, centro_y - radio - 3),
        (centro_x + 7, centro_y - radio - 5),
        (centro_x + 5, centro_y - radio - 1)
    ])

def dibujar_serpiente(serpiente, dx, dy):
    for index, bloque in enumerate(serpiente):
        bx = bloque[0] * TAMANO_BLOQUE
        by = bloque[1] * TAMANO_BLOQUE
        
        if index == 0:
            # --- DISEÑO DE LA CABEZA ---
            pygame.draw.ellipse(pantalla, (60, 150, 65), (bx, by, TAMANO_BLOQUE, TAMANO_BLOQUE))
            
            centro_x = bx + TAMANO_BLOQUE // 2
            centro_y = by + TAMANO_BLOQUE // 2
            
            if dx != 0: 
                pygame.draw.circle(pantalla, (255, 255, 255), (centro_x + dx*4, by + 5), 3)
                pygame.draw.circle(pantalla, (0, 0, 0), (centro_x + dx*5, by + 5), 1.5)
                pygame.draw.circle(pantalla, (255, 255, 255), (centro_x + dx*4, by + TAMANO_BLOQUE - 5), 3)
                pygame.draw.circle(pantalla, (0, 0, 0), (centro_x + dx*5, by + TAMANO_BLOQUE - 5), 1.5)
            elif dy != 0:
                pygame.draw.circle(pantalla, (255, 255, 255), (bx + 5, centro_y + dy*4), 3)
                pygame.draw.circle(pantalla, (0, 0, 0), (bx + 5, centro_y + dy*5), 1.5)
                pygame.draw.circle(pantalla, (255, 255, 255), (bx + TAMANO_BLOQUE - 5, centro_y + dy*4), 3)
                pygame.draw.circle(pantalla, (0, 0, 0), (bx + TAMANO_BLOQUE - 5, centro_y + dy*5), 1.5)
        else:
            # --- DISEÑO DEL CUERPO ---
            reduccion = min(index // 2, 4) 
            grosor = TAMANO_BLOQUE - reduccion
            offset = reduccion // 2
            
            color_cuerpo = COLOR_SERPIENTE if index % 2 == 0 else (67, 160, 71)
            
            pygame.draw.ellipse(pantalla, color_cuerpo, (bx + offset, by + offset, grosor, grosor))

def mostrar_puntuacion(puntuacion):
    fuente_score = pygame.font.SysFont("gothamblack", 19, bold=True)
    texto_score = fuente_score.render(f"SCORE: {puntuacion}", True, (200, 200, 200))
    
    superficie_fondo = pygame.Surface((texto_score.get_width() + 10, texto_score.get_height() + 6))
    superficie_fondo.set_alpha(150)
    superficie_fondo.fill((143, 143, 143))
    
    pantalla.blit(superficie_fondo, (8, 8))
    pantalla.blit(texto_score, (13, 11))

def juego():
    serpiente = [[10, 10]]
    dx, dy = 1, 0
    puntuacion = 0
    velocidad = 5 

    def generar_comida():
        while True:
            pos = [random.randint(0, CUADRICULA - 1), random.randint(0, CUADRICULA - 1)]
            if pos not in serpiente:
                return pos

    comida = generar_comida()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif evento.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0
                elif evento.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif evento.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1

        nueva_cabeza = [serpiente[0][0] + dx, serpiente[0][1] + dy]
        serpiente.insert(0, nueva_cabeza)

        if (nueva_cabeza[0] < 0 or nueva_cabeza[0] >= CUADRICULA or
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= CUADRICULA):
            if sonido_game_over:
                sonido_game_over.play()
            break
            
        # Choque con el cuerpo
        if nueva_cabeza in serpiente[1:]:
            if sonido_game_over:
                sonido_game_over.play()
            break

        # Verificar si come la manzana
        if nueva_cabeza == comida:
            puntuacion += 10
            if sonido_comer:
                sonido_comer.play()
            comida = generar_comida()
            if puntuacion % 30 == 0:
                velocidad += 1
        else:
            serpiente.pop()

        pantalla.fill(COLOR_FONDO)
        dibujar_manzana(comida[0], comida[1])
        dibujar_serpiente(serpiente, dx, dy)
        mostrar_puntuacion(puntuacion)

        pygame.display.flip()
        reloj.tick(velocidad)

    pantalla_game_over(puntuacion)

def pantalla_game_over(puntuacion_final):
    fuente = pygame.font.SysFont("gothambold", 60)
    texto = fuente.render(f"Game Over! Score: {puntuacion_final}", True, COLOR_TEXTO)
    texto_reiniciar = pygame.font.SysFont("gothamlight", 40).render("Press the SPACE to reset", True, COLOR_TEXTO_2)
    
    while True:
        pantalla.fill(COLOR_FONDO)
        pantalla.blit(texto, (TAMANO_PANTALLA // 2 - texto.get_width() // 2, TAMANO_PANTALLA // 3))
        pantalla.blit(texto_reiniciar, (TAMANO_PANTALLA // 2 - texto_reiniciar.get_width() // 2, TAMANO_PANTALLA // 2))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    juego()

pantalla_inicio() 
juego()
