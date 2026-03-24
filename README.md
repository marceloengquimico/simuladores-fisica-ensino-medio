# simuladores-fisica-ensino-medio

# 🔬 Simuladores de Física — Ensino Médio

> Ferramentas interativas para visualizar e compreender conceitos de **Física** do Ensino Médio.  
> Desenvolvidas em Python, com interface gráfica, animações em tempo real e foco didático.

---

## 📦 Simuladores disponíveis

### 🪐 Simulador de Cinemática
**Arquivo:** `fisica_simulador.py`

Simula os quatro tipos de movimento estudados no Ensino Médio:

| Modo | Descrição |
|------|-----------|
| Queda Livre | Objeto liberado do repouso sob ação da gravidade |
| Lançamento Vertical | Objeto lançado para cima ou para baixo |
| Lançamento Horizontal | Objeto lançado paralelamente ao solo |
| Lançamento Oblíquo | Objeto lançado com ângulo configurável |

**Recursos:**
- ⚙️ Gravidade configurável: `g = 10` (simplificado para provas) ou `g = 9,81` (Terra real)
- 🪐 Simulação em outros planetas: Mercúrio, Vênus, Lua, Marte, Júpiter, Saturno, Urano, Netuno e Plutão
- 🐢 Câmera lenta — de `0,05×` até `5×` a velocidade real
- 📐 Equações horárias exibidas em tempo real para cada modo
- 📊 Gráficos de Vy × t, h × t e Vx × t atualizados durante a animação
- 🌍 Tabela comparativa do tempo de queda entre todos os planetas
- Vetor velocidade animado sobre a trajetória

---

### 🪞 Simulador de Espelhos
**Arquivo:** `espelhos_simulador.py`

Demonstra a formação de imagens nos três tipos de espelhos:

| Tipo | Característica |
|------|---------------|
| Plano | Imagem sempre virtual, direita e de mesmo tamanho |
| Côncavo | Imagem varia conforme a posição do objeto em relação a F e C |
| Convexo | Imagem sempre virtual, direita e reduzida |

**Recursos:**
- 📏 Cálculo automático pela **Lei de Gauss**: `1/f = 1/p + 1/q`
- 🔍 **Lei do Aumento**: `M = −q/p` com classificação da imagem
- 🎨 Diagrama de raios com os **3 raios notáveis** desenhados e identificados por cor
- 🧮 Classificação completa: tipo (real/virtual), orientação, tamanho
- 📋 Tabela dos casos notáveis do espelho côncavo como referência rápida
- Sliders interativos para distância do objeto, focal e altura

---

## 🖥️ Como executar

### Pré-requisitos

- Python 3.10 ou superior → [python.org/downloads](https://python.org/downloads)
- Instale as dependências:

```bash
pip install -r requirements.txt
```

### Rodando direto pelo Python

```bash
python fisica_simulador.py
python espelhos_simulador.py
```

### Gerando o executável (.exe)

```bash
python build.py
```

O executável será gerado na pasta `dist/` e pode ser aberto **sem precisar instalar o Python**.

---

## 📚 Conteúdos do currículo cobertos

**Cinemática**
- Movimento Uniformemente Variado (MUV)
- Queda livre e lançamentos
- Equações horárias de posição e velocidade
- Decomposição vetorial de velocidades

**Óptica Geométrica**
- Reflexão da luz
- Espelhos esféricos e planos
- Lei de Gauss para espelhos
- Lei do aumento transversal
- Raios notáveis e diagrama de formação de imagem

---

## 🛠️ Tecnologias utilizadas

| Biblioteca | Uso |
|------------|-----|
| `tkinter` | Interface gráfica (incluso no Python) |
| `matplotlib` | Gráficos e animações |
| `numpy` | Cálculos numéricos |
| `PyInstaller` | Geração do executável |

---

## 📁 Estrutura do repositório

```
📦 simuladores-fisica-ensino-medio/
├── fisica_simulador.py      # Simulador de cinemática
├── espelhos_simulador.py    # Simulador de espelhos
├── build.py                 # Script para gerar executável
├── requirements.txt         # Dependências do projeto
└── README.md
```

---

## 💡 Motivação

Este projeto nasceu da vontade de transformar conceitos abstratos da Física em experiências visuais e interativas. Em vez de resolver equações no papel sem saber o que está acontecendo, o aluno pode **ver** o movimento, **ajustar** os parâmetros e **observar** como cada variável afeta o resultado — em tempo real.

A ideia é simples: aprender Física é muito mais fácil quando você consegue enxergar a Física.

---

## 📄 Licença

Projeto de uso livre para fins educacionais.
