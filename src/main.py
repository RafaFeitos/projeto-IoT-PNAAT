import machine
import time

# ---------------------------------------------------------------------------
# Configuração de hardware
# ---------------------------------------------------------------------------
PIN_LED_EDGE  = 2   # LED verde  — ativo durante inferencia local
PIN_LED_CLOUD = 4   # LED amarelo — ativo durante requisicao para nuvem
PIN_ADC_CENA  = 34  # Potenciometro — entrada de complexidade da cena (0-4095)

led_edge  = machine.Pin(PIN_LED_EDGE,  machine.Pin.OUT)
led_cloud = machine.Pin(PIN_LED_CLOUD, machine.Pin.OUT)
adc_cena  = machine.ADC(machine.Pin(PIN_ADC_CENA))
adc_cena.atten(machine.ADC.ATTN_11DB)  # Faixa completa 0-3.3V

# ---------------------------------------------------------------------------
# Constantes do sistema
# ---------------------------------------------------------------------------
LIMIAR_COMPLEXIDADE = 0.70  # Acima disso, inferencia local é insuficiente
LATENCIA_EDGE_MS    = 12    # Tempo simulado de inferencia local (ms)
LATENCIA_NUVEM_MS   = 180   # Tempo simulado de round-trip para nuvem (ms)
PAUSA_VISUALIZACAO  = 800   # Pausa adicional para LED ser visivel no Wokwi
CICLOS_SIMULACAO    = 6     # Ciclos fixos — garante encerramento limpo no CI
ADC_MAX             = 4095  # Resolucao 12-bit do ADC do ESP32

# ---------------------------------------------------------------------------
# Avaliacao de complexidade da cena
# ---------------------------------------------------------------------------
def ler_complexidade_cena():
    """
    Le o valor ADC do potenciometro e retorna a
    complexidade normalizada da cena entre 0.0 e 1.0.
    """
    leitura = adc_cena.read()
    return leitura / ADC_MAX


def avaliar_modo(score_complexidade):
    """
    Retorna o modo de inferencia com base no limiar de complexidade.
    EDGE: processamento local suficiente e preferivel.
    NUVEM: complexidade excede capacidade de processamento embarcado.
    """
    if score_complexidade >= LIMIAR_COMPLEXIDADE:
        return "NUVEM"
    return "EDGE"

# ---------------------------------------------------------------------------
# Controle dos LEDs por estado
# ---------------------------------------------------------------------------
def definir_leds(modo):
    if modo == "EDGE":
        led_edge.value(1)
        led_cloud.value(0)
    else:
        led_edge.value(0)
        led_cloud.value(1)


def desligar_leds():
    led_edge.value(0)
    led_cloud.value(0)

# ---------------------------------------------------------------------------
# Telemetria serial
# ---------------------------------------------------------------------------
def registrar(ciclo, score, modo, latencia_ms):
    print("[CICLO {:02d}] complexidade={:.2f} | modo={} | latencia={}ms".format(
        ciclo, score, modo, latencia_ms
    ))

# ---------------------------------------------------------------------------
# Execucao principal
# ---------------------------------------------------------------------------
print("SYSTEM READY")
print("Sistema de decisao Edge/Cloud — prototipo de veiculo autonomo")
print("limiar={} | ciclos={}".format(LIMIAR_COMPLEXIDADE, CICLOS_SIMULACAO))
print("---")

for ciclo in range(1, CICLOS_SIMULACAO + 1):
    score    = ler_complexidade_cena()
    modo     = avaliar_modo(score)
    latencia = LATENCIA_EDGE_MS if modo == "EDGE" else LATENCIA_NUVEM_MS

    definir_leds(modo)
    time.sleep_ms(latencia)           # Simula tempo real de processamento
    registrar(ciclo, score, modo, latencia)
    time.sleep_ms(PAUSA_VISUALIZACAO) # Pausa para LED ser visivel no Wokwi

desligar_leds()
print("---")
print("SIMULATION COMPLETE")
