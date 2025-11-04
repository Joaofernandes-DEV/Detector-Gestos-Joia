# 📸 Detector de Gestos "Joia" (Thumbs-Up Detector)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-red.svg)

Um projeto em Python que utiliza Visão Computacional (OpenCV e MediaPipe) para detectar o gesto "Joia" (👍) em tempo real através da webcam do usuário.

Ao reconhecer o gesto, o aplicativo sobrepõe uma imagem customizável na tela, fornecendo um feedback visual imediato.

---

### 📷 Demonstração

> ![Demo do Projeto](assets/video_DetectorDeJoias.mp4)

---

## 📋 Sumário

- [Principais Funcionalidades](#-principais-funcionalidades)
- [Tech Stack](#-tech-stack)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Execução](#-instalação-e-execução)
- [Como Funciona](#-como-funciona)
- [Como Contribuir](#-como-contribuir)
- [Licença](#-licença)

---

## ✨ Principais Funcionalidades

- **Detecção em Tempo Real:** Captura e processa o feed da webcam frame a frame.
- **Rastreamento de Mão:** Utiliza a solução `mp.solutions.hands` do MediaPipe para identificar 21 pontos de referência (landmarks) da mão.
- **Lógica de Gesto Personalizada:** Implementa uma função `is_thumbs_up` que valida o gesto analisando as coordenadas relativas dos landmarks dos dedos.
- **Feedback Visual Imediato:** Sobrepõe uma imagem (PNG com transparência ou JPG) na tela assim que o gesto é detectado.

---

## 🛠️ Tech Stack

Este projeto é construído primariamente com as seguintes bibliotecas:

- **Python 3.8+**
- **OpenCV** (`opencv-python`): Para captura de vídeo, manipulação de frames e exibição da imagem.
- **MediaPipe** (`mediapipe`): Para a detecção de mãos e seus pontos de referência.

---

## 📂 Estrutura do Projeto

## 📂 Estrutura do Projeto

O repositório está organizado da seguinte forma para garantir manutenibilidade:

/Detector-Gestos-Joia
│
├── 📁 assets
│ ├── joia.png
│ └── Contém todos os arquivos de mídia (imagens, etc.)
│
├── 📁 src
│ ├── main.py
│ └── Código-fonte principal da aplicação
│
├── .gitignore # Especifica arquivos a serem ignorados pelo Git
├── CONTRIBUTING.md # Diretrizes para contribuição (opcional)
├── LICENSE # Licença open-source do projeto (opcional)
├── requirements.txt # Lista de dependências Python
└── README.md # Esta documentação

---

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

### Pré-requisitos

- Python 3.8 ou superior
- Uma webcam conectada

### Passos

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/](https://github.com/)[SEU-USUARIO-GITHUB]/Detector-Gestos-Joia.git
    cd Detector-Gestos-Joia
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**

    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar no Windows
    .\venv\Scripts\activate

    # Ativar no macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o script:**
    O script principal deve ser executado a partir do diretório raiz do projeto para que os caminhos para a pasta `assets` funcionem corretamente.

    ```bash
    python src/main.py
    ```

5.  **Teste:**
    - Uma janela do OpenCV deve abrir, mostrando sua webcam.
    - Faça o gesto de "Joia" (👍) para a câmera.
    - A imagem `joia.png` deve aparecer na tela.
    - Pressione a tecla **'q'** para fechar.

---

## 🧠 Como Funciona

A detecção não utiliza um modelo de IA treinado para o gesto específico. Em vez disso, ela aplica uma lógica de coordenadas (heurística) sobre os _landmarks_ fornecidos pelo MediaPipe:

1.  **Dedos Fechados:** Verifica se as pontas dos 4 dedos (indicador, médio, anelar e mínimo) estão com uma coordenada Y _menor_ (mais abaixo na tela) do que suas respectivas juntas do meio (PIP).
2.  **Polegar Aberto:** Verifica se a ponta do polegar (TIP) está com uma coordenada Y _maior_ (mais acima na tela) do que sua junta inferior (IP).
3.  **Validação:** O gesto é considerado "Joia" somente se os 4 dedos estiverem fechados E o polegar estiver aberto.

---

## 🤝 Como Contribuir

Contribuições são o que tornam a comunidade open-source um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito bem-vinda**.

Se você tiver uma sugestão para melhorar este projeto, por favor, faça um fork do repositório e crie um pull request. Você também pode simplesmente abrir uma "Issue" com a tag "melhoria" (enhancement).

Por favor, leia o arquivo `CONTRIBUTING.md` para mais detalhes sobre o código de conduta e o processo para submeter pull requests.

---

## 📄 Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.
