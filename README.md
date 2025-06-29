# 🎮 Checkers Voice Project

Este projeto propõe um jogo de damas acessível controlado por voz.
Ele utiliza a biblioteca Vosk para reconhecimento de fala totalmente offline,
permitindo a execução em um Raspberry Pi 3 sem depender da internet.
A interface em Pygame foi desenvolvida com foco em acessibilidade e
oferece controle redundante por mouse e voz. O projeto contribui com a
pesquisa em jogos acessíveis e abre espaço para melhorias futuras, como
feedback auditivo, oponente mais sofisticado e estudos com usuários
reais.

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

4. Baixe o modelo de voz em português do Brasil do Vosk (por exemplo,
`vosk-model-small-pt-0.3`) e extraia o conteúdo em `assets/model/`. Caso a
 pasta ainda não exista, crie-a. Os modelos de voz estão disponíveis em:
[https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

5. Execute o jogo com controle por voz:
```bash
python src/main.py
```

## 🧪 Executar testes

Instale a dependência de testes e rode o `pytest` a partir do diretório do projeto:

```bash
pip install pytest
pytest
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

## 📄 Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

Desenvolvido por [evil988](https://github.com/evil988)
