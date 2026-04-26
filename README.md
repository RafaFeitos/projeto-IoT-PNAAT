# Processo Seletivo – Intensivo Maker | IoT
## Etapa Prática – Sistemas Embarcados

Bem-vindo(a) à **etapa prática do processo seletivo para o Intensivo Maker | IoT**.

Esta atividade tem como objetivo avaliar suas competências em **Sistemas Embarcados**, com foco em **organização de projeto, lógica de firmware e simulação de hardware**, a partir da aplicação prática dos conhecimentos adquiridos nos cursos EAD da etapa anterior.

> 🎯 **Objetivo principal**  
> Avaliar sua capacidade de **planejar, estruturar e desenvolver** uma solução funcional de sistemas embarcados, seguindo boas práticas de engenharia.

---

## 🏁 Passo 0 – Antes de Tudo

Se você **nunca utilizou Git ou GitHub**, não se preocupe.  
Siga atentamente os passos abaixo — eles fazem parte do processo de aprendizagem esperado.

---

### 1️⃣ Criação de Conta no GitHub

1. Acesse: https://github.com  
2. Clique em **Sign up**  
3. Crie sua conta gratuita seguindo as instruções da plataforma  

> 📌 O GitHub será utilizado para:
> - Envio do seu projeto  
> - Versionamento do código  
> - Correção e validação automática via GitHub Actions  

---

### 2️⃣ Instalação do Git

O **Git** é a ferramenta responsável pelo controle de versões do seu código.

### Windows
Baixe e instale o **Git Bash**:  
https://git-scm.com/downloads

### Linux / macOS
Verifique se o Git já está instalado:

```bash
git --version
```
> Caso não esteja, instale pelo gerenciador de pacotes do seu sistema.

## ⚙ Passo 1 – Preparando o Ambiente

Para desenvolver o desafio, você deverá criar uma cópia deste repositório no seu GitHub.

### 1️⃣ Fork do Repositório
No canto superior direito desta página, clique em Fork

<img width="219" height="45" alt="image" src="https://github.com/user-attachments/assets/5d629626-513a-445c-ba0f-e5bb3e225187" />


Uma cópia do repositório será criada no seu perfil do GitHub

> 🔎 O Fork permite que você trabalhe de forma independente, sem alterar o repositório original do processo seletivo.

### 2️⃣ Clone do Repositório

No repositório do seu Fork, clique em **<> Code**

<img width="149" height="52" alt="image" src="https://github.com/user-attachments/assets/abbd331b-a005-4633-89c6-afd16acbe828" />

Copie a URL e execute no terminal:

```bash
git clone https://github.com/SEU_USUARIO/nome-do-repositorio.git
cd nome-do-repositorio
```

> O comando git clone cria uma cópia local do repositório para desenvolvimento.

### 3️⃣ Preparação do Ambiente de Execução

Você pode executar o projeto de duas formas. Escolha apenas uma.

#### 🔹 Opção A – Ambiente Python Local

**Requisitos:**

- Python 3.10 ou 3.11
- pip

**Instale as dependências:**

```bash
pip install -r requirements.txt
```

#### 🔹 Opção B – Dev Container (Recomendado)

Este repositório inclui um Dev Container, garantindo um ambiente padronizado.

**Requisitos:**

- VS Code
- Docker instalado
- Extensão Dev Containers

**Passos:**

1. Abra o repositório no VS Code
2. Clique em “Reopen in Container”
3. Aguarde a criação automática do ambiente

> ➡️ Todas as dependências serão instaladas automaticamente.

## 🔐 Passo 2 – Criando sua API Key do Wokwi

A simulação do projeto será executada automaticamente via GitHub Actions, utilizando o Wokwi CLI.

Para isso, você precisa gerar uma API Key.

1. Acesse: https://wokwi.com/dashboard/ci
2. Faça login (Google ou GitHub)
3. Clique em Generate API Token
4. Copie a chave gerada (exemplo: wokwi-xxxxxxxx)

>⚠️ Importante
- Nunca faça commit dessa chave
- Ela deve ser armazenada apenas como secret no GitHub

## 🔒 Passo 3 – Configurando a API Key no GitHub (Secrets)

**No repositório do seu Fork:**

1. Vá em Settings
2. Acesse Secrets and variables → Actions
3. Clique em New repository secret
4. Nome: WOKWI_API_KEY
5. Valor: sua chave gerada
6. Salve

> ✔️ As GitHub Actions do template já estão preparadas para usar essa variável automaticamente.

## 🧠 Passo 4 – Desafio Técnico

Você deverá desenvolver um projeto de sistemas embarcados simulados, utilizando Python e Wokwi.

### 📁 Estrutura mínima esperada

```text
/project
 ├── src/
 │   └── main.py        # Código principal do projeto
 ├── wokwi.toml         # Configuração da simulação
 ├── diagram.json       # Circuito no Wokwi
 └── README.md          # Explicação do seu projeto
```

> Você pode expandir essa estrutura se desejar, desde que mantenha os arquivos essenciais.

# Sistema de Decisão Adaptativa Edge/Cloud para Veículos Autônomos

## 👤 Identificação do Candidato

- **Nome completo:** Rafael Silva Arraes Feitosa
- **GitHub:** https://github.com/RafaFeitos

---

## 1️⃣ Visão Geral da Solução

Em veículos autônomos, sensores como câmeras, LiDAR e radar produzem continuamente grandes volumes de dados que precisam ser processados em tempo real para que o veículo tome decisões seguras. Entretanto, o processamento local embarcado possui limitações de energia, capacidade computacional e custo de hardware.

Uma alternativa é realizar o **offloading computacional**, enviando parte das tarefas para servidores externos ou para a nuvem. O problema é que essa decisão não pode ser fixa, pois as condições da estrada mudam constantemente. Em cenários simples, o processamento local pode ser suficiente. Em cenários complexos, com baixa visibilidade ou maior densidade de tráfego, pode ser necessário transferir o processamento para um ambiente com maior poder computacional.

O desafio acadêmico consiste em decidir, em tempo real, quando manter o processamento no veículo e quando migrá-lo para a nuvem sem causar atrasos que comprometam a segurança.

Este projeto surgiu como desdobramento prático da minha iniciação científica sobre deploy Edge/Cloud vehicular, na qual estudei os limites e trade-offs do processamento distribuído em veículos autônomos. O protótipo implementa um ESP32 que monitora continuamente as condições do ambiente e decide de forma autônoma entre processamento local (EDGE) e offloading para nuvem (NUVEM), com resposta em tempo real e estabilidade garantida por histerese.

**Durante a simulação:**
- 🟢 **LED verde** — processamento local ativo
- 🟡 **LED amarelo** — offloading para nuvem ativo
- 🎛️ **Potenciômetro** — representa a variação das condições do ambiente
- 📟 **Serial monitor** — telemetria estruturada em tempo real

---

## 2️⃣ Arquitetura do Sistema Embarcado

O sistema é organizado em um loop principal orientado por tempo com `time.ticks_ms()`, garantindo resposta contínua sem bloqueios de execução.

**Fluxo principal:**

```
Sensor ADC
    ↓
Leitura suavizada (média de 4 amostras)
    ↓
Cálculo do score de complexidade
    ↓
Decisão com histerese
    ↓
[score > 0.58] → CLOUD_OFFLOAD → LED amarelo + log de envio
[score < 0.48] → EDGE_INFERENCE → LED verde + log local
[0.48 ≤ score ≤ 0.58] → MANTÉM ESTADO ATUAL (zona neutra)
    ↓
Latência não bloqueante simulada
    ↓
Telemetria serial → novo ciclo
```

**Estrutura de estados:**

```
EDGE_INFERENCE  ←→  CLOUD_OFFLOAD
       ↑                  ↑
  score < 0.48       score > 0.58

  [zona neutra: mantém estado atual]
```

A latência não bloqueante permite que o sistema continue monitorando o sensor durante a simulação do tempo de processamento — se as condições mudarem durante uma requisição para nuvem, o sistema responde imediatamente sem aguardar o fim do ciclo.

---

## 3️⃣ Componentes Utilizados na Simulação

| Componente | Função |
|------------|--------|
| ESP32 DevKit C v4 | Controlador principal — executa a lógica de decisão |
| Potenciômetro (ADC D34) | Simula variação das condições de visibilidade da via |
| LED verde (D2) | Indica modo EDGE — inferência processada localmente |
| LED amarelo (D4) | Indica modo NUVEM — tarefa enviada para processamento remoto |
| Resistores 220Ω | Proteção dos LEDs |
| WiFi Wokwi-GUEST | Simula o canal de comunicação com o servidor remoto |
| Serial monitor | Saída de telemetria estruturada em tempo real |

---

## 4️⃣ Decisões Técnicas Relevantes

### Histerese com dois limiares distintos

A lógica de decisão utiliza dois limiares independentes:

- `LIMIAR_NUVEM = 0.58` — entrada no modo cloud
- `LIMIAR_EDGE = 0.48` — retorno ao modo edge

Essa separação de 10 pontos cria uma zona de estabilidade intermediária na qual pequenas oscilações do sensor não provocam trocas de modo. O sistema só muda de estado quando há uma variação clara e intencional no ambiente — comportamento análogo ao de sistemas embarcados reais que precisam de estabilidade nas decisões de controle. Em sistemas veiculares reais, comutações excessivas entre edge e cloud gerariam overhead de rede e instabilidade no comportamento do veículo.

### Latência não bloqueante

A latência de processamento foi implementada sem interromper o monitoramento do sensor. Durante a simulação do round-trip para nuvem (180ms), o loop continua lendo o ADC e pode alterar o modo imediatamente se as condições mudarem — garantindo responsividade em tempo real mesmo durante eventos de offloading.

### Suavização do ADC por média amostral

A leitura do sensor utiliza média de 4 amostras consecutivas para reduzir ruído elétrico do ADC, evitando decisões baseadas em variações instantâneas espúrias — prática padrão em firmware embarcado para leitura de sinais analógicos.

### Loop orientado por tempo com ticks_ms

O loop principal utiliza `time.ticks_ms()` em vez de ciclos fixos, permitindo que o sistema opere de forma contínua e responsiva. Essa abordagem é mais adequada para sistemas embarcados que precisam reagir a eventos externos em tempo indeterminado.

### Limitação do potenciômetro

O potenciômetro foi utilizado como mecanismo de simulação para representar a variação do ambiente externo. Em produção, essa entrada seria substituída por dados reais de sensores de percepção — câmeras, LiDAR ou métricas de qualidade de conexão da própria interface de rede.

### Ajuste do timeout no CI

O timeout padrão do Wokwi CI foi aumentado de 10s para 120s no arquivo `.github/workflows/ci.yml`. Essa alteração foi necessária porque a simulação opera por 40 segundos para demonstrar adequadamente a alternância entre modos. A modificação foi documentada conforme orientação do processo seletivo, sendo uma limitação do ambiente de CI e não da solução em si.

---

## 5️⃣ Resultados Obtidos

O sistema funcionou conforme o esperado:

-  Decisão autônoma e contínua entre EDGE e NUVEM em tempo real
-  Resposta imediata à variação do sensor sem aguardar fim de ciclo
-  Estabilidade garantida pela histerese — sem oscilações na zona intermediária
-  LEDs alternando corretamente conforme o modo ativo
-  WiFi simulado conectado com sucesso via rede Wokwi-GUEST
-  Telemetria estruturada registrada no serial monitor a cada leitura

Ao final de cada sessão o sistema imprime um resumo de execução com o total de trocas de modo e o percentual de tempo em cada estado. Em uma sessão de 40 segundos com variação do sensor, o sistema registrou:

```
RESUMO DA SESSAO
trocas=8 | edge=71% | nuvem=29%
```

Esses dados evidenciam que a decisão adaptativa funcionou conforme o esperado. A predominância do modo EDGE é intencional — em veículos autônomos, o processamento local é sempre preferível por reduzir latência e consumo de banda. O offloading para nuvem é acionado apenas quando a complexidade do ambiente cruza claramente o limiar superior (0.58), retornando ao modo local assim que as condições melhoram. Esse comportamento assimétrico é uma característica do design, não uma limitação.

**Para reproduzir a simulação:** inicie com o potenciômetro posicionado à esquerda (baixa complexidade — modo EDGE). Gire gradualmente para a direita até o score ultrapassar 0.58 para acionar o modo NUVEM. O sistema responde em tempo real e o log registra cada transição automaticamente. Os valores de `edge%` e `nuvem%` no resumo final variam conforme a interação com o sensor durante a sessão.

---

## 6️⃣ Comentários Adicionais

### Dificuldades encontradas

A principal dificuldade foi garantir responsividade em tempo real do sensor sem recorrer a delays bloqueantes. A solução com `ticks_ms` e latência não bloqueante resolveu o problema de forma limpa, mas exigiu reestruturação do loop principal em relação à abordagem inicial com ciclos fixos.

### Limitações da solução

O protótipo resolve a lógica central da decisão adaptativa, mas a origem da entrada ainda está simplificada. O potenciômetro representa manualmente o que em produção seria gerado automaticamente por sensores reais. A decisão de manter essa simplificação foi consciente — o objetivo foi demonstrar a arquitetura de decisão, não reproduzir toda a infraestrutura de percepção de um veículo autônomo.

### Melhorias com mais tempo

A principal evolução seria substituir a entrada manual pelo monitoramento automático da qualidade do canal de comunicação — latência, RSSI ou throughput disponível — permitindo que o próprio módulo de conectividade influencie a decisão de offloading sem intervenção externa. Em hardware real com módulo 5G integrado ao ESP32, essa métrica estaria disponível nativamente, tornando o sistema completamente autônomo.

Outras melhorias possíveis:
- Envio real por MQTT para servidor de inferência remoto
- Coleta histórica de métricas para análise de desempenho
- Comparação entre diferentes políticas de offloading
- Integração com pipeline de percepção real

### Contexto acadêmico

A problemática abordada neste projeto está diretamente relacionada à minha iniciação científica, na qual estudei os limites do processamento distribuído em veículos autônomos com base no artigo **FogWise: On the limits of the coexistence of heterogeneous applications on Fog computing and Internet of Vehicles** (Mendonça Júnior et al., 2021), que investiga como a heterogeneidade afeta a capacidade do Vehicular Fog Computing de atender requisitos de aplicações com restrições de latência.

O protótipo desenvolvido neste desafio representa uma implementação embarcada simplificada do problema central estudado no FogWise — a decisão adaptativa entre processamento local e remoto considerando as condições do ambiente.

> 💡 **Referência:** Mendonça Júnior, F. F. et al. *FogWise: On the limits of the coexistence of heterogeneous applications on Fog computing and Internet of Vehicles*. Transactions on Emerging Telecommunications Technologies, 2021. DOI: [10.1002/ett.4145](https://onlinelibrary.wiley.com/doi/abs/10.1002/ett.4145)

---

## 🆘 Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores

Boa sorte no processo seletivo.
Mostre sua capacidade de pensar como um engenheiro de sistemas embarcados.
****
