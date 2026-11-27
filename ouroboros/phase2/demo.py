"""Demonstração offline: um quadro sintético de 4 × 4 pixels."""
from .baseline.feistel16 import decrypt_block, encrypt_block

KEY = 0x01234567
FRAME = ("0110", "1111", "1001", "1001")


def show(word):
    bits = f"{word:016b}"
    pixels = bits.translate(str.maketrans("01", ".#"))
    print("\n".join(pixels[start:start + 4] for start in range(0, 16, 4)))


def main():
    plain = int("".join(FRAME), 2)
    packet = encrypt_block(plain, KEY).to_bytes(2, "big")

    print(f"Emissor · quadro original (0x{plain:04X})")
    show(plain)
    print(f"\nCanal simulado · dois bytes ({packet.hex(' ').upper()})")

    received = int.from_bytes(packet, "big")
    decoded = decrypt_block(received, KEY)
    print("\nReceptor · quadro recuperado")
    show(decoded)

    changed = decrypt_block(received ^ 1, KEY)
    print("\nReceptor · após alterar um bit no canal")
    show(changed)
    print("\nO bloco alterado também virou um quadro. O Feistel não autentica a mensagem.")


if __name__ == "__main__":
    main()
