import machine
import time
import network

# -------------------------------------------------
# HARDWARE
# -------------------------------------------------
PIN_LED_EDGE  = 2   # LED verde — ativo durante inferencia local
PIN_LED_CLOUD = 4   # LED amarelo — ativo durante offloading para nuvem
PIN_ADC       = 34  # Potenciometro — representa visibilidade da via

led_edge  = machine.Pin(PIN_LED_EDGE,  machine.Pin.OUT)
led_cloud = machine.Pin(PIN_LED_CLOUD, machine.Pin.OUT)

adc = machine.ADC(machine.Pin(PIN_ADC))
adc.atten(machine.ADC.ATTN_11DB)  # Faixa 0-3.3V

ADC_MAX = 4095  # ADC de 12 bits

# -------------------------------------------------
# CONFIGURACAO
# -------------------------------------------------
LATENCIA_EDGE  = 12   # Tempo simulado de inferencia local (ms)
LATENCIA_NUVEM = 180  # Tempo simulado de round-trip para nuvem (ms)

# Histerese: dois limiares distintos evitam comutacoes excessivas
# em zona intermediaria — comportamento analogo a sistemas reais
LIMIAR_EDGE  = 0.48  # Abaixo disso, retorna para modo EDGE
LIMIAR_NUVEM = 0.58  # Acima disso, entra em modo NUVEM

# Pesos da formula de complexidade
# Visibilidade tem peso dominante pois impacta diretamente
# a qualidade da inferencia local em tempo real
PESO_VIS = 0.55
PESO_DEN = 0.30
PESO_VEL = 0.15

# Valores fixos representando cenario urbano tipico
DENSIDADE  = 0.55
VELOCIDADE = 0.45

INTERVALO_LEITURA = 150   # Intervalo entre leituras do ADC (ms)
TEMPO_TOTAL       = 40000 # Duracao total da simulacao (ms)

SSID     = "Wokwi-GUEST"  # Rede WiFi simulada disponivel no Wokwi
PASSWORD = ""              # Rede aberta no ambiente de simulacao

# -------------------------------------------------
# WIFI
# -------------------------------------------------
def conectar_wifi():
    """
    Conecta ao WiFi do Wokwi.
    Retorna True se a conexao for estabelecida.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    tentativas = 0
    while not wlan.isconnected() and tentativas < 10:
        time.sleep_ms(500)
        tentativas += 1

    if wlan.isconnected():
        print("WiFi conectado IP:", wlan.ifconfig()[0])
        return True

    print("WiFi indisponivel")
    return False

# -------------------------------------------------
# LEITURA SUAVIZADA DO SENSOR
# -------------------------------------------------
def ler_visibilidade():
    """
    Le o potenciometro e normaliza o valor entre 0.0 e 1.0.
    A media de 4 amostras reduz ruido do ADC.
    """
    soma = 0
    for _ in range(4):
        soma += adc.read()
        time.sleep_ms(2)
    return round((soma / 4) / ADC_MAX, 2)

# -------------------------------------------------
# CALCULO DO SCORE
# -------------------------------------------------
def calcular_score(vis):
    """
    Calcula o score de complexidade da cena.
    Combina visibilidade, densidade e velocidade em um unico valor.
    """
    return round(
        (DENSIDADE  * PESO_DEN) +
        (vis        * PESO_VIS) +
        (VELOCIDADE * PESO_VEL),
        2
    )

# -------------------------------------------------
# DECISAO COM HISTERESE
# -------------------------------------------------
def decidir_modo(score, modo_atual):
    """
    Aplica histerese na decisao de modo.
    So muda de estado quando o score ultrapassa um dos limiares,
    evitando comutacoes desnecessarias na zona intermediaria.
    """
    if score >= LIMIAR_NUVEM:
        return "NUVEM"
    if score <= LIMIAR_EDGE:
        return "EDGE"
    return modo_atual  # Zona neutra — mantem estado atual

# -------------------------------------------------
# CONTROLE DOS LEDS
# -------------------------------------------------
def atualizar_leds(modo):
    """Atualiza LEDs conforme o modo de inferencia ativo."""
    if modo == "EDGE":
        led_edge.value(1)
        led_cloud.value(0)
    else:
        led_edge.value(0)
        led_cloud.value(1)

# -------------------------------------------------
# LATENCIA NAO BLOQUEANTE
# -------------------------------------------------
def executar_latencia(modo_atual, duracao_ms, wifi_ok):
    """
    Simula a latencia do processamento sem bloquear o sistema.
    Durante a espera, o sensor continua sendo monitorado.
    """
    inicio = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), inicio) < duracao_ms:
        vis       = ler_visibilidade()
        score     = calcular_score(vis)
        novo_modo = decidir_modo(score, modo_atual)

        if novo_modo != modo_atual:
            atualizar_leds(novo_modo)
            mensagem = "enviando para nuvem..." if novo_modo == "NUVEM" else "retornando para edge..."
            latencia = LATENCIA_NUVEM if novo_modo == "NUVEM" else LATENCIA_EDGE
            print("Mudanca durante latencia -> {}".format(mensagem))
            print("score={} | vis={} | modo={} | latencia={}ms".format(
                score, vis, novo_modo, latencia))
            return novo_modo

        time.sleep_ms(INTERVALO_LEITURA)

    return modo_atual

# -------------------------------------------------
# TELEMETRIA — RESUMO DA SESSAO
# -------------------------------------------------
def imprimir_resumo(trocas, ms_edge, ms_nuvem):
    """
    Imprime resumo da sessao ao final da simulacao.
    Evidencia o comportamento do sistema de forma rastreavel.
    """
    total = ms_edge + ms_nuvem
    if total == 0:
        return

    pct_edge  = round((ms_edge  / total) * 100)
    pct_nuvem = round((ms_nuvem / total) * 100)

    print("RESUMO DA SESSAO")
    print("trocas={} | edge={}% | nuvem={}%".format(
        trocas, pct_edge, pct_nuvem))

# -------------------------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------------------------
print("SYSTEM READY")
print("Sistema Edge/Cloud com resposta em tempo real")
print("---")

wifi_ok = conectar_wifi()
print("---")

modo_atual    = "EDGE"
atualizar_leds(modo_atual)

# Contadores de telemetria
trocas        = 0
ms_edge       = 0
ms_nuvem      = 0
ultimo_tick   = time.ticks_ms()

inicio = time.ticks_ms()

while time.ticks_diff(time.ticks_ms(), inicio) < TEMPO_TOTAL:
    vis       = ler_visibilidade()
    score     = calcular_score(vis)
    novo_modo = decidir_modo(score, modo_atual)

    # Acumula tempo no modo atual antes de qualquer troca
    agora    = time.ticks_ms()
    delta    = time.ticks_diff(agora, ultimo_tick)
    if modo_atual == "EDGE":
        ms_edge += delta
    else:
        ms_nuvem += delta
    ultimo_tick = agora

    if novo_modo != modo_atual:
        trocas    += 1
        modo_atual = novo_modo
        atualizar_leds(modo_atual)
        mensagem = "enviando para nuvem..." if modo_atual == "NUVEM" else "retornando para edge..."
        latencia = LATENCIA_NUVEM if modo_atual == "NUVEM" else LATENCIA_EDGE
        print("Mudanca detectada -> {}".format(mensagem))
        print("score={} | vis={} | modo={} | latencia={}ms".format(
            score, vis, modo_atual, latencia))
        modo_atual = executar_latencia(modo_atual, latencia, wifi_ok)

    else:
        latencia = LATENCIA_NUVEM if modo_atual == "NUVEM" else LATENCIA_EDGE
        print("score={} | vis={} | modo={} | latencia={}ms".format(
            score, vis, modo_atual, latencia))
        time.sleep_ms(INTERVALO_LEITURA)

# -------------------------------------------------
# FINALIZACAO
# -------------------------------------------------
led_edge.value(0)
led_cloud.value(0)
print("---")
imprimir_resumo(trocas, ms_edge, ms_nuvem)
print("---")
print("SIMULATION COMPLETE")
