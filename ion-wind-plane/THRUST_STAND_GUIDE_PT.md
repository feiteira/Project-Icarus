# Thrust Stand — Guia de Construção Completo
## Project Icarus | ~€64 Mínimo Viável | Lisboa/Darmstadt

*Guião tão detalhado como um manual LEGO ou IKEA. Criado para principiantes com electrónica básica.*

---

## PARTE 0: Antes de Começar

### ⚠️ AVISO DE SEGURANÇA — LEIA PRIMEIRO

**Tensão Alta (HV) é perigosa.**
- Este sistema gera 20–50 kV. Isso é MUITO mais do que os 220V da tomada.
- 20kV pode saltar até 1cm pelo ar.
- 50kV pode saltar até 3cm pelo ar.
- Uma descarga de 50kV causa queimadura grave, paragem cardíaca e morte.
- **Nunca** toques nos fios HV quando o sistema está ligado.
- **Sempre** desconecta a fonte antes de mexer nos electrodos.
- Se sentires formigueiro ou vires faíscas, desliga tudo imediatamente.
- Mantém as mãos a pelo menos 10cm dos componentes HV quando ligados.

**O que fazer se houver um acidente:**
1. Desliga a fonte imediatamente
2. Não toques na vítima directamente — usa um objecto isolante (madeira, plástico)
3. Chama emergência

**Não é para ser assustador — é para ser respeitoso.** Com cuidado, não há problema.

### O que vais aprender
- Qual é o thrust real (em mN) que os teus electrodos geram
- Se o design dos electrodos está a funcionar correctamente
- Calibrar o simulador com dados reais
- Se o Project Icarus é viável fisicamente

### Ferramentas necessárias (que provavelmente já tens)
- Multímetro (para medir tensão e continuidade)
- Ferro de soldar (15-30W) + estanho
- Stripadores de fio / alicates
- Fita isoladora (electríca)
- Fita cola quente (hot glue)
- Régua ou paquímetro para medir gap
- Papelão ou placa de corte para base

---

## PARTE 1: Lista de Materiais (BOM)

### Começa por aqui — confirma tudo antes de ligar

| Qtd | Componente | Preço | Required? |
|-----|------------|-------|-----------|
| 1 | ZVS Flyback Module (5–12V input, 20–50kV output) | €10 | ✅ Sim |
| 1 | Arduino Nano Every | €10 | ✅ Sim |
| 1 | Fio stainless steel 0.1–0.2mm (ou tungsténio) | €6 | ✅ Sim |
| 1 | Cobre ou alumínio foil (10cm × 50cm) | €5 | ✅ Sim |
| 1 | Placa acrylic ou polycarbonate (20cm × 30cm × 3mm) | €10 | ✅ Sim |
| 1 | Barra roscada M3 × 20cm (ou pedaços de plástico) | €3 | ✅ Sim |
| 1 | Porcas e anilhas M3 (pack) | €2 | ✅ Sim |
| 1 | Suporte pilhas 18650 × 2 (ou fonte 5–12V) | €8 | ✅ Sim |
| 2 | Pilhas 18650 (se usares suporte) | €0 (tens?) | ✅ Sim |
| 1 | Resistências: 10MΩ + 1MΩ (para divisor HV) | €1 | ✅ Sim |
| 1 | Multímetro (já tens) | €0 | ✅ Sim |
| 1 | Ferro de soldar + estanho | €0 | ✅ Sim |
| 1 | Fita isoladora + cola quente | €0 | ✅ Sim |
| 1 | Caixa de cartão ou madeira para base | €0 | Opcional |
| 1 | Fio de cobre flexível (para conexões HV) | €2 | ✅ Sim |
| 1 | HX711 + Load Cell 5kg | €12 | Opcional |

**Total mínimo viável: ~€64** (sem HX711)

### Notas para Opção B (10× Thrust)

| Qtd | Componente | Preço | Required? |
|-----|------------|-------|-----------|
| 1 | fonte de energia Laptop PSU 19V/3A (para Opção B) | €0–15 | Opcional |
| 1 | Segundo ZVS flyback secondary ou módulo dual-output (para Opção B tandem) | €10–15 | Opcional |

---

## Configuration Options — Choose Your Path

There are two configurations for the thrust stand. Both use the same basic setup. Choose based on your goals and available power supply.

### Option A: Starter / Validation (~EUR64)
- Voltage: 35 kV
- Gap: 20 mm (safe, no arcing risk)
- Electrode length: 500 mm
- Collector: NACA airfoil (copper foil molded around tube)
- Power: ~15W (small ZVS module, EUR10-15)
- Expected thrust: 169 mN
- T/W @ 100g: 1.69 (flight viable)
- Risk: Very low. Gap is safe even for beginners.
- Build time: 1-2 hours

**Best for:** First build, validation, learning the physics.

### Option B: Upgrade / 10× Thrust (~EUR80 + laptop PSU)
- Voltage: 35 kV
- Gap: 8 mm (borderline, requires care)
- Electrode length: 500 mm
- Collector: NACA airfoil
- Power: ~50W (laptop PSU 19V/3A or similar)
- Expected thrust: 1627 mN (9.6× more than Option A!)
- T/W @ 100g: 16 (extreme performance)
- Risk: Higher arcing risk at 8mm. Only proceed after validating with Option A first.
- Requires: Two ZVS flyback secondaries or one high-power module
- Build time: 3-4 hours

**Best for:** If you want to test the tandem concept and push toward flight-capable thrust.

---

## PARTE 2: Conhecer os Componentes

### 2.1 ZVS Flyback Module (Gerador HV)

**O que é:** Uma pequena placa que recebe 5–12V DC e transforma em 20–50kV AC (depois multiplicado).

**Como identificar:** Tem um transformador flybackcastanho/vermelho no centro, 2 bobinas laterais, e 4 terminais (2 de input, 2 de output HV).

**Cores dos fios típicos:**
- Vermelho = VCC (5–12V input +)
- Preto = GND (terra/negativo)
- Fios HV = branco e preto (altatensão output)

[NOTA: Os fios HV são perigosos — nunca os toques com as mãos quando ligado!]

**O que faz:** Cria a alta tensão necessária para ionizar o ar entre os electrodos e gerar o "vento iónico".

### 2.2 Arduino Nano Every

**O que é:** Um pequeno computador programável que vais usar para ler tensão e fazer logging de dados.

**Como identificar:** Placa azul ou verde, 4.5cm × 1.8cm, com porta USB-mini e pinos laterais.

**O que faz:** Mede tensões, comunica com o computador, controla o sistema.

### 2.3 Fio Emitter (Alta Tensão)

**O que é:** Fio muito fino (0.1–0.2mm de diâmetro). Quanto mais fino, mais fácil de gerar corona.

**Tipo recomendado:** Stainless steel 0.1mm (mais barato e mais fácil de encontrar) ou tungsténio 0.1mm (melhor performance).

**O que faz:** O fio emitter é o electrodo positivo (ânodo). Quando energizado, arranca electrões do ar à sua volta, criando iões que são acelerados para o collector — isso é o "vento iónico".

### 2.4 Collector Foil (Foil de Cobre ou Alumínio)

**O que é:** Folha de cobre ou alumínio, fina (0.05–0.1mm), com superficie lisa.

**O que faz:** É o electrodo negativo (cátodo). Os iões acelerados colidem com o ar junto ao collector, transferem momento, e geram thrust na direcção do collector.

[NOTA: O collector deve ser LISO — sem arestas vivas. Qualquer ponta afiada causa arcing (faíscas) em vez de corona.]

### 2.5 Resistências (Divisor HV)

**O que é:** Duas resistências — 10MΩ (10 mega-ohms) e 1MΩ (1 mega-ohm) — ligadas em série.

**O que faz:** O divisor resistivo reduz a alta tensão para uma tensão medida pelo multímetro/Arduino. Se 10MΩ + 1MΩ estão em série, a tensão no ponto intermédio é 1/11 da tensão total.

**Esquema:**
```
  HV (+) ----[10MΩ]----+----[1MΩ]---- HV (-)
                         |
                     AO ARDUINO
                   (ou multimetro)
```

### 2.6 Acrylic/Polycarbonate (Estrutura)

**O que é:** Placa plástica isolante, 3mm de espessura, 20cm × 30cm.

**O que faz:** Suporta os electrodos electricamente isolados um do outro. O acrylic é bom isolante eléctrico e resiste a arcos superficiais.

---

## PARTE 3: Montagem — Passo a Passo

### 3.1 Montagem do Gerador HV (ZVS Flyback)

**Passo 1: Identifica os terminais do ZVS**

Olha para o módulo ZVS. Tens 4 terminais pequenos ou parafusos:
- **INPUT**: 2 terminais (GND e VCC)
- **OUTPUT HV**: 2 terminais grossos ou fichas (HV+ e HV-)

[NOTA: Os fios HV de output são os dois fios grossos que saem do transformador flyback. Por vezes têm pontas nu-as — usa fita isoladora para cobrir tudo excepto 2cm da ponta!]

**Passo 2: Liga o input (5–12V DC)**

O ZVS precisa de tensão contínua entre 5V e 12V. Podes usar:
- Suporte de 2× 18650 em série (7.4V) — **recomendado para começar**
- Fonte de laboratório 5–12V
- Qualquer fonte DC que dê pelo menos 2A

**Polaridade:**
- **VCC (+)**: liga ao positivo da fonte (ou vermelho do suporte 18650)
- **GND (-)**: liga ao negativo/terra

[⚠️ AVISO: Se ligares ao contrário, o módulo pode aquecer e partir. Verifica sempre antes de ligar!]

**Passo 3: Testa o módulo**

1. Liga a fonte de alimentação
2. O ZVS deve começar a emitir um zumbido agudo ( tipo transformador)
3. **Se não ouvirshum:** Verifica as ligações, polaridade, e tensão da fonte
4. **Se o módulo aquecer muito (>50°C ao toque):** Desliga imediatamente — pode estar avariado ou sobrecarga

**Passo 4: Medir a tensão HV**

Para saber quanta tensão estás a gerar, usa o divisor resistivo:

1. Liga a resistência de **10MΩ** directamente a um dos fios HV output
2. Liga a resistência de **1MΩ** em série (do outro lado da 10MΩ até ao outro fio HV)
3. O ponto intermédio (onde as duas resistências se encontram) liga ao pino **A0** do Arduino (ou ao multímetro DC na escala de baixa tensão)
4. A tensão no ponto intermédio = Tensão HV / 11

[NOTA: Multímetro como alternativa — pões o multímetro entre o ponto intermédio e o GND. Se marcar 2.7V, a HV real é ~30kV.]

### 3.2 Montagem dos Electrodos

**Passo 1: Prepara a estrutura base**

1. Corta o acrylic em 4 peças:
   - 2 peças de **15cm × 3cm** (montantes verticais)
   - 2 peças de **20cm × 3cm** (base e topo)
2. Faz 4 furos de 3mm em cada montante (para os parafusos M3)

**Passo 2: Monta a estrutura em "sandwich"**

```
[Base acrylic] ─ [Montante esquerdo] ─ [Emitter wire] ─ [Montante direito] ─ [Base acrylic]
```

1. Coloca os 2 montants verticais perpendiculares à base, separados por ~5cm (vais ajustar depois)
2. Usa M3 porcas e anilhas para fixar — não apertes demasiado

**Passo 3: Monta o fio emitter (electrodo positivo/ânodo)**

1. Passa o fio stainless steel (0.1mm) entre os dois montants, a meio da estrutura
2. Estica o fio — deve estar tenso como a corda de uma guitarra, mas não ao ponto de partir
3. A tensão correcta é: o fio não deve tocar em nada, deve estar completamente esticado e direito
4. Fixa o fio com fita isoladora ou knots nas pontas — não uses nada condutivo!

[NOTA: Se o fio estiver demasiado frouxo, vai vibrar e partir. Se estiver demasiado esticado, pode partir com mudanças de temperatura. Tensão média é o ideal.]

**Passo 4: Monta o collector foil**

1. Corta uma tira de cobre/alumínio com ~2cm de largura e 15cm de comprimento
2. Moldura suavemente à volta de um tubo ou cilindro (para ficar com forma arredondada)
3. Coloca o collector paralelo ao fio emitter, com os dois a apontarem na mesma direcção
4. O gap (espaço) entre o fio emitter e o collector deve ser:
   - **Opção A (Starter): 20mm** — seguro, sem risco de arcing (podes usar uma régua ou um pedaço de cartão de 2cm como espaçador)
   - **Opção B (Upgrade/10×): 8mm** — cuidado, tens de validar primeiro com Opção A

[⚠️ AVISO (Opção A): Se o gap for < 15mm, vais ter arcing (faíscas) em vez de corona. Se for > 40mm, o thrust vai ser muito fraco. 20mm é o ponto óptimo para começar.]
[⚠️ AVISO (Opção B): Com 8mm, o risco de arcing é maior. Só avança para este gap após teres validado o sistema em Opção A (20mm). Se ouvires estalos, volta a 10mm ou mais.]

**Passo 5: Liga os fios HV**

1. Fio HV+ (do ZVS) → Liga ao fio emitter (electrodo positivo/ânodo)
2. Fio HV- (do ZVS) → Liga ao collector foil (electrodo negativo/cátodo)

[NOTA: Usa fio de cobre flexível para estas ligações. Faz uma boa soldadura — uma ligação mal feita vai criar um ponto quente e pode causar arcing.]

### 3.3 Medição de Thrust (Método do Pêndulo)

O método do pêndulo é simples e não precisa de load cell.

**Princípio:** Se o electrodo está pendurado e o vento iónico o empurra, podes medir o ângulo de deflexão e calcular a força.

**Passo 1: Constrói o suporte do pêndulo**

1. Prende um fio de nylon ou corda fina (20–30cm) ao topo da estrutura dos electrodos
2. Pendura o conjunto num pivô (pode ser um lápis atravessado entre duas mesas, ou um prego numa parede)
3. O pêndulo deve poder oscilar livremente num plano horizontal

**Passo 2: Calibração com pesos conhecidos**

Antes de ligar o HV, calibra o sistema:

1. Pega em pesos pequenos: porcas M3 (cada uma pesa ~1.5g), clips de papel, pequenas peças metálicas
2. hanging weights horizontalmente no fio do pêndulo
3. Mede quanto é que o pêndulo se desloca para o lado com cada peso
4. Faz uma tabela:

| Peso adicionado | Deflexão (mm) |
|----------------|--------------|
| 0 (sem peso) | 0 mm |
| 1× porca M3 (~1.5g) | ~3 mm |
| 2× porca M3 (~3g) | ~6 mm |
| 5× porca M3 (~7.5g) | ~15 mm |

[NOTA: A deflexão depende do comprimento do fio do pêndulo. Quanto mais curto o fio, maior a deflexão para o mesmo peso.]

**Passo 3: Mede a deflexão com HV ligado**

1. Liga o ZVS e aumenta lentamente a tensão
2. Observa o pêndulo — começa a deflectir na direcção do collector (o lado oposto ao emitter)
3. Regista:
   - Tensão HV (kV) — lida no divisor + multímetro
   - Deflexão máxima (mm)
   - somethings estranhos (faíscas visíveis, cheiro, zumbido anormal)

**Passo 4: Converte deflexão em thrust (mN)**

Formula simplificada para um pêndulo com fio de comprimento L e deflexão x:

```
Thrust (mN) ≈ (deflexão_mm / 1000) × ( peso_total_g × 9.81 ) × ( L_gap / L_pendulum )
```

Exemplo: Se L_pendulum = 250mm, deflexão = 5mm, peso da estrutura = 50g:
```
Thrust ≈ (5/1000) × (50 × 9.81) × (25/250)
Thrust ≈ 0.025 × 490.5 × 0.1
Thrust ≈ 1.2 mN
```

[NOTA: Esta é uma aproximação. Para medições precisas, usa o método do Polk 2017 com calibração formal.]

### 3.4 Ligação do Arduino (Data Logging)

**Se só quiseres medir tensão (mínimo viável):**

1. Liga o ponto intermédio do divisor HV ao pino **A0** do Arduino Nano
2. Liga o **GND** do Arduino ao **GND** do ZVS (terra comum)
3. Liga o Arduino ao computador por USB
4. Abre o Arduino IDE e usa o "Serial Monitor" a 9600 baud

**Código mínimo (Copy-paste para Arduino IDE):**

```cpp
void setup() {
  Serial.begin(9600);
}
void loop() {
  int raw = analogRead(A0);
  float voltageHV = raw * (11.0 / 1023.0) * (5.0 / 1023.0) * 1000; // × 11 divisor
  // Se multímetro: voltageHV = raw * 5.0 / 1023.0 * 11;
  Serial.print("Tensão HV: ");
  Serial.print(voltageHV, 1);
  Serial.println(" kV");
  delay(500);
}
```

**Se usares HX711 + Load Cell (para thrust directo):**

1. Liga HX711 ao Arduino:
   - VCC → 5V
   - GND → GND
   - DT → pino D2
   - SCK → pino D3
2. Instala a library HX711 no Arduino IDE (Sketch → Include Library → Manage Libraries → "HX711")
3. Usa um código de exemplo da library para calibrar

---

## PARTE 4: Primeiro Teste

> **Nota para Opção B:** Começa SEMPRE por validar o sistema em Opção A (gap 20mm) antes de reduzir para 8mm. Não pules esta etapa — o arcing a 8mm pode danificar os electrodos e o módulo ZVS.

### O que procurar

**Tensão inicial:** Começa por verificar — quantos kV estás a gerar com o divisor?

**Liga o sistema e:**
1. **Observa**: Vês um brilho roxo/azul muito fraco à volta do fio emitter? Isso é corona — bom sinal!
2. **Ouve**: Zumbido agudo constante é normal. Se ouvires "crack" ou faíscas (estalo), há arcing — aumenta o gap.
3. **Cheira**: Cheiro a ozono (como após trovoada) é normal. Se cheirares a queimado, desliga.

### Como distinguir corona de arcing

| Sinal | Corona (bom ✓) | Arcing (mau ✗) |
|-------|----------------|----------------|
| Visão | Brilho roxo suave | Faíscas brilhantes |
| Som | Zumbido agudo constante | Estalos ou crepitações |
| Odor | Ozono suave | Ozono muito forte + queimado |
| Thrust | Medido no pêndulo | Thrust cai, arcing consome energia |

**Se tiver arcing:**
- Aumenta o gap (de 20mm para 30-35mm)
- Verifica que o collector está liso (sem pontas)
- Limpa o fio emitter (pode ter poeira ou gordura)

### O que registar

Faz uma tabela no teu caderno de laboratório:

| Tensão (kV) | Gap (mm) | Deflexão (mm) | Thrust (mN) | Notas |
|-------------|----------|---------------|-------------|-------|
| 20 | 25 | 2 | 0.5 | Sem arcing |
| 25 | 25 | 4 | 1.0 | Corona OK |
| 30 | 25 | 6 | 1.5 | Corona OK |
| 35 | 25 | 8 | 2.0 | Limiar de arcing |
| 40 | 30 | 10 | 2.5 | OK |

---

## PARTE 5: Resolução de Problemas

| Problema | Causa provável | Solução |
|----------|--------------|--------|
| Sem corona a nenhuma tensão | Fio emitter muito grosso (>0.3mm) | Substitui por fio mais fino (0.1mm) |
| Sem corona a nenhuma tensão | ZVS não está a funcionar | Verifica input com multímetro; se 0V, problema na fonte |
| Corona fraca, pouco thrust | Gap demasiado grande (>40mm) | Reduz gap para 20mm |
| Corona fraca, pouco thrust | Humidade elevada | Funciona pior em dias húmidos — testa em dias secos |
| Arcing constante | Gap demasiado pequeno (<15mm) | Aumenta gap |
| Arcing constante | Collector com pontas | Lima ou dobra para alisar |
| ZVS aquece muito | Tensão input demasiado alta (>12V) | Reduz para 5V |
| ZVS aquece muito | ZVS avariado ou demasiado pequeno | Troca por um ZVS de maior potência |
| Thrust cai ao fim de minutos | Emissor sobreaquece | Desliga 5 min, limpa, volta a testar |
| Medições inconsistentes | Pêndulo encravado | Verifica que oscila livremente |
| Medições inconsistentes | Humidade no ar | Seca o setup com luz solar ou aquecedor |

---

## APÊNDICE A: Diagrama de Circuito

```
                          DIVISOR HV
  FONTE 5-12V              (10MΩ + 1MΩ)
  ┌─────────┐
  │  ZVS    │ HV+ ───────────────────────────┐
  │ FLYBACK │                                 │
  │ MODULE  │                                 │
  └─────────┘                              ┌──┴──┐
       │                                   │ A0  │ Arduino
  HV- ─┴───────────────────────────────────┤     │ Nano
                                          └──┬──┘
                                             │
  ELECTRODOS ─────────────────────────────────┴───── GND
  ┌─────────────────────────────────────────────────┐
  │  ┌─────────────┐         ┌─────────────┐        │
  │  │   EMITTER   │  GAP    │  COLLECTOR  │        │
  │  │  (fio 0.1mm)│ ←20mm→ │ (foil liso) │        │
  │  │    (HV+)    │         │    (GND)    │        │
  │  └─────────────┘         └─────────────┘        │
  │     fio SUSPENDIDO no pêndulo                    │
  └─────────────────────────────────────────────────┘
       ↑
       │ fio nylon
       ○ pivô (lápis/prego)
       ↓
   [Counterweight calibrado]
```

## APÊNDICE B: Vídeos de Referência

**Integza — Ionic Plasma Thruster:**
https://www.youtube.com/watch?v=mnCvmxt2jn8

**Plasma Channel — Ionic Thrust Wing:**
https://www.youtube.com/watch?v=5lDSSgHG4q0

**Polk 2017 Thrust Measurement (paper):**
https://pubmed.ncbi.nlm.nih.gov/33510551/

## APÊNDICE C: Glossário

- **Corona discharge**: Ionização suave do ar à volta de um fio/ponteiro energizado. Produz vento iónico sem faíscas.
- **Arcing (estilha)**: Descarga disruptiva entre electrodos. Produz faíscas visíveis e NÃO gera thrust útil.
- **EHD (ElectroHydroDynamics)**: Estudo da interacção entre campos eléctricos e fluidos (ar). É a física por detrás do vento iónico.
- **Ion wind**: Movimento de ar causado por iões acelerados num campo eléctrico.
- **Emitter (ânodo)**: Electrodo positivo que emite iões. Deve ser pontiagudo/filo.
- **Collector (cátodo)**: Electrodo negativo que recebe os iões. Deve ser liso e arredondado.
- **Gap**: Distância entre emitter e collector. 20-40mm é a gama segura para evitar arcing.
- **Streamer**: Forma de corona que aparece como filamentos visíveis no ar (excitação óptica).
- **Thrust stand**: Estrutura para medir thrust directamente (força em mN).
- **ZVS (Zero Voltage Switching)**: Técnica eficiente de comutação para Flyback transformers.

---

*Guia criado por Clawdia01 como parte do Project Icarus*
*Versão: 1.0 | Data: Abril 2026*
