# 🎮 Checkers Voice Project

Este projeto aplica **reconhecimento de voz ao jogo de damas** com o objetivo de torná-lo acessível para pessoas com deficiência motora.

## 🧠 Tecnologias utilizadas

- [Vosk](https://alphacephei.com/vosk/) – reconhecimento de voz offline
- PyAudio – captura de áudio do microfone
- Pygame – interface gráfica do jogo

## ▶️ Como executar

1. Clone o repositório:
```bash
git clone https://github.com/evil988/checkers-voice.git
cd checkers-voice
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Baixe um modelo Vosk e extraia para `assets/model/`. Modelos disponíveis em:
[https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

5. Execute o jogo com controle por voz:
```bash
python src/main.py
```

## 🎯 Comandos de voz aceitos

- `linha três coluna quatro` → destaca a casa (3,4)
- Ao dizer outro comando válido em seguida, movimenta a peça da casa destacada para a nova casa.
- `cancelar` → remove o destaque atual (se houver)

## 🕹️ Funcionalidades atuais

- Destaca casas via voz (ex: "linha dois coluna três")
- Move peças por voz com regras básicas de movimento
- Cancela seleção com o comando "cancelar"
- Validação visual com destaque colorido
- Feedback textual no terminal

## 📁 Estrutura

```
checkers-voice/
├── src/main.py              # Módulo principal
├── checkers/                # Regras e desenho do tabuleiro
├── menu/                    # Menu principal por voz
├── speech/                  # Reconhecimento de fala
├── assets/model/            # Modelo Vosk (baixar separadamente)
├── tests/                   # Testes unitários
└── requirements.txt
```

---

Desenvolvido por [evil988](https://github.com/evil988)
