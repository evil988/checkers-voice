from test_voice import escutar_comando

if __name__ == "__main__":
    print("Iniciando reconhecimento de voz (modular)...")
    try:
        while True:
            comando = escutar_comando()
            if comando:
                print("🎤 Comando recebido:", comando)
    except KeyboardInterrupt:
        print("\nEncerrando reconhecimento de voz.")
