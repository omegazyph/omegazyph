def vigenere_brute_force(ciphertext):
    # Iterate through all possible key lengths
    for key_length in range(1, len(ciphertext) + 1):
        possible_key = ""
        possible_plaintext = ""

        # Repeat the key to match the length of the ciphertext
        for i in range(len(ciphertext)):
            possible_key += chr((i % key_length) + ord('A'))

        # Decrypt the ciphertext using the possible key
        for i in range(len(ciphertext)):
            char = ciphertext[i]
            shift = ord(possible_key[i]) - ord('A')

            if char.isalpha():
                if char.islower():
                    decrypted_char = chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
                else:
                    decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
                possible_plaintext += decrypted_char
            else:
                possible_plaintext += char

        print(f"Key Length: {key_length}, Possible Key: {possible_key}, Decrypted Text: {possible_plaintext}")


# Example usage:
ciphertext = "LXFOPVEFRNHR"
vigenere_brute_force(ciphertext)
