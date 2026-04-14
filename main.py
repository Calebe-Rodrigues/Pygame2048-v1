import pygame
import random
import sys

pygame.init()

# Configurações do jogo, incluindo dimensões da janela, tamanho do tabuleiro, cores e fontes
LARGURA_JANELA = 500
ALTURA_JANELA = 600
TAMANHO_GRADE = 4
TAMANHO_CELULA = 100
BORDA_CELULA = 10
MARGEM_TOPO = 100
COR_DE_FUNDO = (187, 173, 160)
COR_DO_TEXTO = (119, 110, 101)
TEXT0_CLARO = (249, 246, 242)

# Dicionário que mapeia os valores das peças para suas cores correspondentes, com um valor padrão para peças maiores que 2048
CORES_CELULAS = {
    0: (205, 192, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Tamanhos das fontes dos números. Números maiores precisam ter uma fonte menor para caberem dentro da célula
FONTE_GRANDE = pygame.font.Font(None, 55)
FONTE_MEDIA = pygame.font.Font(None, 40)
FONTE_PEQUENA = pygame.font.Font(None, 30)


# Criando a janela do jogo e o relógio para controlar a taxa de atualização
janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
clock = pygame.time.Clock()


# Função para inicializar o estado do jogo, criando o tabuleiro e adicionando as peças iniciais
def iniciar_jogo():

    # O conteúdo do tabuleiro é representado por uma matriz 4x4,
    # onde cada célula pode conter um número (2, 4, 8, etc.) ou 0 para indicar que está vazia.
    tabuleiro = [[0] * TAMANHO_GRADE for _ in range(TAMANHO_GRADE)]

    # Adiciona duas peças iniciais no tabuleiro, chamando a função
    adicionar_celula(tabuleiro)
    adicionar_celula(tabuleiro)

    # Retorna um dicionário com o estado do jogo, incluindo o tabuleiro
    # e o status de movimento (moveu)
    return {
        "tabuleiro": tabuleiro,  # Matriz 4x4 representando o estado atual do tabuleiro
        "moveu": False,  # Indica se houve um movimento na última ação do jogador, usado para determinar se uma nova peça deve ser adicionada
    }


# Função para adicionar uma nova peça (2 ou 4) em uma célula vazia do tabuleiro
def adicionar_celula(tabuleiro):
    celulas_vazias = [] # Lista para armazenar as posições das células vazias no tabuleiro

    # Percorre o tabuleiro para encontrar células vazias (com valor 0) e armazena suas posições
    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            if tabuleiro[i][j] == 0:            # Se a célula estiver vazia (valor 0)
                celulas_vazias.append((i, j))   # Adiciona a posição da célula vazia à lista celulas_vazias

    # Se houver células vazias, escolhe uma aleatoriamente e atribui a ela o valor 2 ou 4
    if celulas_vazias:
        i, j = random.choice(celulas_vazias)

        # A função random.choice é usada para escolher aleatoriamente um item do array [2, 2, 2, 2, 4] para ser adicionado ao tabuleiro
        # 2 aparece quatro vezes no array para que a probabiliade de escolher 2 seja quatro vezes maior do que escolher 4
        tabuleiro[i][j] = random.choice([2, 2, 2, 2, 4])

# Função para comprimir os números em uma linha,
# removendo os zeros e movendo os números para o inicio da linha,
# preenchendo o restante com zeros
def comprimir(linha):
    # Remove zeros colcando os números no inicio da linha
    nova_linha = [x for x in linha if x != 0]

    # preenchendo o restante com zeros
    nova_linha += [0] * (TAMANHO_GRADE - len(nova_linha))
    return nova_linha


# Função para mesclar os números em uma linha, somando os números iguais adjacentes e atualizando a pontuação
def mesclar(linha):
    # Percorre a linha e verifica se há números iguais adjacentes (diferentes de zero),
    # se houver, soma os números e zera o número adjacente
    for i in range(TAMANHO_GRADE - 1):
        if linha[i] == linha[i + 1] and linha[i] != 0: # Se os números adjacentes são iguais e diferentes de zero
            linha[i] *= 2                              # Soma os números (multiplica por 2)
            linha[i + 1] = 0                           # Zera o número adjacente para indicar que foi mesclado
    return linha


# Função para mover os números para a esquerda,
# comprimindo e mesclando as linhas,
# e atualizando o status de movimento
def mover_esquerda(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for i in range(TAMANHO_GRADE):
        linha_original = tabuleiro[i] # Armazena a linha original para comparação posterior

        tabuleiro[i] = comprimir(tabuleiro[i])
        tabuleiro[i] = mesclar(tabuleiro[i])
        tabuleiro[i] = comprimir(tabuleiro[i])

        # Se a linha resultante for diferente da linha original, 
        # isso indica que houve um movimento (números foram movidos ou mesclados),
        if tabuleiro[i] != linha_original:
            estado_de_jogo["moveu"] = True # A variável "moveu" é utilizada mais tarde para determinar se uma nova peça deve ser adicionada 


# Mesma coisa para a direita, mas
# invertendo a linha antes de comprimir e mesclar,
# e invertendo novamente depois
def mover_direita(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for i in range(TAMANHO_GRADE):
        linha_original = tabuleiro[i] # Armazena a linha original para comparação posterior

        # Inverte a linha para tratar o movimento para a direita como se fosse para a esquerda
        # A notação [::-1] separa uma "fatia" do array seguindo a lógica de [início:fim:passo]
        # Ou seja, o passo -1 indica que o array deve ser percorrido de trás para frente, invertendo a ordem dos elementos
        tabuleiro[i] = tabuleiro[i][::-1] 

        tabuleiro[i] = comprimir(tabuleiro[i])
        tabuleiro[i] = mesclar(tabuleiro[i])
        tabuleiro[i] = comprimir(tabuleiro[i])
        tabuleiro[i] = tabuleiro[i][::-1] # Inverte novamente a linha para restaurar a ordem original dos elementos

        if tabuleiro[i] != linha_original:
            estado_de_jogo["moveu"] = True


# Para mover para cima ou para baixo, precisamos trabalhar com as colunas do tabuleiro,
# extraindo as colunas, comprimindo e mesclando como se fossem linhas
def mover_cima(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for j in range(TAMANHO_GRADE):

        # Extraindo a coluna j do tabuleiro
        coluna_original = [tabuleiro[i][j] for i in range(TAMANHO_GRADE)]

        # Criando uma cópia da coluna para comparação posterior
        coluna = coluna_original

        coluna = comprimir(coluna)
        coluna = mesclar(coluna)
        coluna = comprimir(coluna)
        
        # Aqui utilizamos um for normal ao invés de list comprehension para atualizar a coluna do tabuleiro
        # pois precisamos do valor de i tanto em tabuleiro[i][j] quanto em coluna[i]
        for i in range(TAMANHO_GRADE):
            tabuleiro[i][j] = coluna[i] 

        if coluna != coluna_original:
            estado_de_jogo["moveu"] = True


def mover_baixo(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    estado_de_jogo["moveu"] = False
    for j in range(TAMANHO_GRADE):

        coluna_original = [tabuleiro[i][j] for i in range(TAMANHO_GRADE)]

        coluna = coluna_original

        coluna = coluna[::-1]
        coluna = comprimir(coluna)
        coluna = mesclar(coluna)
        coluna = comprimir(coluna)
        coluna = coluna[::-1]

        for i in range(TAMANHO_GRADE):
            tabuleiro[i][j] = coluna[i]
        if coluna != coluna_original:
            estado_de_jogo["moveu"] = True


# Função para mover os números em uma direção específica (esquerda, direita, cima ou baixo),
# chamando a função de movimento correspondente
def mover(direction, estado_de_jogo):
    if direction == "left":
        mover_esquerda(estado_de_jogo)
    elif direction == "right":
        mover_direita(estado_de_jogo)
    elif direction == "up":
        mover_cima(estado_de_jogo)
    elif direction == "down":
        mover_baixo(estado_de_jogo)

    # Se houve um movimento, adiciona uma nova peça
    if estado_de_jogo["moveu"]:
        adicionar_celula(estado_de_jogo["tabuleiro"])


# Função para desenhar o estado do jogo na tela,
# incluindo o tabuleiro e as peças
def desenhar_jogo(estado_de_jogo):
    tabuleiro = estado_de_jogo["tabuleiro"]
    janela.fill((250, 248, 246))

    # Título do jogo
    titulo = FONTE_GRANDE.render("2048", True, COR_DO_TEXTO)
    janela.blit(titulo, (20, 20))

    # Calcula a posição do tabuleiro para centralizá-lo na tela
    tabuleiro_top = MARGEM_TOPO
    tabuleiro_left = (LARGURA_JANELA - (TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA)) // 2

    # Desenha o fundo do tabuleiro, criando um retângulo maior para dar um efeito de borda
    pygame.draw.rect(
        janela,                                                                       # Surperficie onde desenhar
        COR_DE_FUNDO,                                                                 # Cor do retângulo
        (
            tabuleiro_left - 5,                                                       # Posição x do retângulo (com margem para borda)
            tabuleiro_top - 5,                                                        # Posição y do retângulo (com margem para borda)
            TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA + 10, # Largura do retângulo (tamanho do tabuleiro + margem para borda)
            TAMANHO_GRADE * TAMANHO_CELULA + (TAMANHO_GRADE - 1) * BORDA_CELULA + 10, # Altura do retângulo (tamanho do tabuleiro + margem para borda)
        ),
    )

    # Desenha as peças do tabuleiro, iterando sobre cada célula
    # desenhando um retângulo com a cor correspondente ao valor da peça,
    # e desenhando o número da peça centralizado dentro do retângulo
    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            x = tabuleiro_left + j * (TAMANHO_CELULA + BORDA_CELULA) # Calcula posição x da célula
            y = tabuleiro_top + i * (TAMANHO_CELULA + BORDA_CELULA)  # Calcula posição y da célula

            valor = tabuleiro[i][j]

            # Obtém a cor correspondente ao valor da peça,
            # usando o dicionário CORES_CELULAS (com um valor padrão para peças maiores que 2048)
            color = CORES_CELULAS.get(valor, CORES_CELULAS[2048])

            # Desenha o retângulo da peça com a cor correspondente
            pygame.draw.rect(janela, color, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))

            # Se a peça não for vazia (valor diferente de 0), desenha o número da peça centralizado dentro do retângulo
            if valor != 0:
                if valor <= 4:                                                  # Se o valor for menor ou igual a 4 utilizamos a fonte grande
                    texto = FONTE_GRANDE.render(str(valor), True, COR_DO_TEXTO)
                elif valor < 1024:                                              # Se o valor for menor que 1024 utilizamos a fonte média
                    texto = FONTE_MEDIA.render(str(valor), True, COR_DO_TEXTO)
                else:                                                           # Para valores maiores ou iguais a 1024 utilizamos a fonte pequena
                    texto = FONTE_PEQUENA.render(str(valor), True, TEXT0_CLARO)

                texto_rect = texto.get_rect(
                    center=(x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)
                )
                janela.blit(texto, texto_rect)

    # Exibe instruções na parte inferior da tela
    legenda = [
        FONTE_PEQUENA.render(
            "Use WASD ou as setas para movimentar", True, (150, 150, 150)
        ),
        FONTE_PEQUENA.render("R para reiniciar", True, (150, 150, 150)),
    ]

    # Funções que escrevem as intruções na tela
    janela.blit(legenda[0], (tabuleiro_left, ALTURA_JANELA - 55))
    janela.blit(legenda[1], (tabuleiro_left, ALTURA_JANELA - 30))

    # Atualiza a tela para mostrar as mudanças feitas
    pygame.display.flip() 


def main():
    estado_de_jogo = iniciar_jogo() 
    pygame.display.set_caption("Pygame 2048") # Define o título da janela do jogo


    running = True

    # Game loop principal, que continua rodando enquanto a variável running for True,
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Verifica se uma tecla foi pressionada e chama a função de movimento correspondente
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    mover("left", estado_de_jogo)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    mover("right", estado_de_jogo)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    mover("up", estado_de_jogo)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    mover("down", estado_de_jogo)

                # Se a tecla R for pressionada, reinicia o jogo chamando a função iniciar_jogo
                elif event.key == pygame.K_r:
                    estado_de_jogo = iniciar_jogo()

                # Se a tecla Q for pressionada, encerra o jogo definindo running como False
                elif event.key == pygame.K_q:
                    running = False

        # Desenha o estado atual do jogo na tela e controla a taxa de atualização
        desenhar_jogo(estado_de_jogo)
        clock.tick(60) # Limita o jogo a 60 frames por segundo

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

