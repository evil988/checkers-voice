# 🎮 Checkers Voice Project

Este projeto aplica **reconhecimento de voz ao jogo de damas** com o objetivo de torná-lo acessível para pessoas com deficiência motora.

## 🧠 Tecnologias utilizadas

- [Vosk](https://alphacephei.com/vosk/) – reconhecimento de voz offline
- PyAudio – captura de áudio do microfone
- Pygame – interface gráfica do jogo

## ▶️ Como executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Certifique-se de que o modelo Vosk está em `assets/model/`. Você pode baixá-lo [aqui](https://alphacephei.com/vosk/models).

3. Execute o projeto:
```bash
python3 main.py
```

## 🎯 Comandos de voz aceitos

- `mover linha dois coluna três` → move a peça da posição (2,3) para frente

## 📁 Estrutura

```
checkers_voice_project/
├── main.py
├── recognition/        # Reconhecimento de voz (Vosk)
├── game/               # Jogo de damas (Pygame)
└── assets/model/       # Modelo de linguagem Vosk
```

---

Desenvolvido por [evil988](https://github.com/evil988)
