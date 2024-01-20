import secrets
import json

# Function to generate a random non-repeating pattern for encryption/decryption
def generate_random_pattern(length, max_shift):
    return [secrets.randbelow(max_shift) + 1 for _ in range(length)]

# Function to create substitution maps for each shift value in the pattern
def create_substitution_maps(shift, max_shift, is_letter_map):
    if is_letter_map:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
        return dict(zip(alphabet, shifted_alphabet))
    else:
        digits = "0123456789"
        shifted_digits = digits[shift:] + digits[:shift]
        return dict(zip(digits, shifted_digits))

# Cache substitution maps for all possible shifts
def cache_substitution_maps(max_shift, is_letter_map):
    cache = {}
    if is_letter_map:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for shift in range(max_shift):
            shifted_alphabet = alphabet[shift:] + alphabet[:shift]
            cache[shift] = dict(zip(alphabet, shifted_alphabet))
    else:
        digits = "0123456789"
        for shift in range(max_shift):
            shifted_digits = digits[shift:] + digits[:shift]
            cache[shift] = dict(zip(digits, shifted_digits))
    return cache

# Updated encryption function using the cache
def encrypt_with_pattern_updated(data, pattern, is_letter, substitution_map_cache):
    max_shift = 26 if is_letter else 10
    result = []
    for i, char in enumerate(data):
        if (char.isalpha() if is_letter else char.isdigit()):
            shift = pattern[i % len(pattern)] % max_shift
            substitution_map = substitution_map_cache[shift]
            new_char = substitution_map[char.upper() if is_letter else char]
            result.append(new_char.lower() if char.islower() else new_char)
        else:
            result.append(char)
    return ''.join(result)

# Updated decryption function using the cache
def decrypt_with_pattern_updated(data, pattern, is_letter, substitution_map_cache):
    max_shift = 26 if is_letter else 10
    result = []
    for i, char in enumerate(data):
        if (char.isalpha() if is_letter else char.isdigit()):
            shift = (-pattern[i % len(pattern)]) % max_shift
            substitution_map = substitution_map_cache[shift]
            new_char = substitution_map[char.upper() if is_letter else char]
            result.append(new_char.lower() if is_letter and char.islower() else new_char)
        else:
            result.append(char)
    return ''.join(result)

# Functions to save and load the patterns to/from a file
def save_patterns_to_file(patterns, file_path):
    with open(file_path, 'w') as file:
        json.dump(patterns, file)

def load_patterns_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def vigenere_cipher_for_numbers(pattern, keyword):
    keyword_numbers = [(ord(char) - ord('A')) for char in keyword.upper()]
    keyword_length = len(keyword_numbers)
    max_shift = 26  # Assuming the pattern is for letters, use 10 for digits
    vigenere_pattern = [(shift + keyword_numbers[i % keyword_length]) % max_shift for i, shift in enumerate(pattern)]
    return vigenere_pattern

def inv_vigenere_cipher_for_numbers(pattern, keyword):
    keyword_numbers = [(ord(char) - ord('A')) for char in keyword.upper()]
    keyword_length = len(keyword_numbers)
    max_shift = 26  # Assuming the pattern is for letters, use 10 for digits
    original_pattern = [(shift - keyword_numbers[i % keyword_length]) % max_shift for i, shift in enumerate(pattern)]
    return original_pattern

# Main script execution
if __name__ == "__main__":
    # Specify the maximum length of the recovery keys
    max_length = 160

    # Generate random patterns for letters and digits
    letter_pattern = generate_random_pattern(max_length, 26)  # Alphabet has 26 letters
    digit_pattern = generate_random_pattern(max_length, 10)   # Digits range from 0 to 9

    # Generate substitution map cache
    letter_substitution_map_cache = cache_substitution_maps(26, True)
    digit_substitution_map_cache = cache_substitution_maps(10, False)

    # Encryption demonstration
    recovery_key = "ExampleRecoveryKey1-2-3-4-5"  # Replace with your actual key
    # Encrypt with letter pattern and then with digit pattern, using the caches
    encrypted_key_letters = encrypt_with_pattern_updated(recovery_key, letter_pattern, True, letter_substitution_map_cache)
    encrypted_key = encrypt_with_pattern_updated(encrypted_key_letters, digit_pattern, False, digit_substitution_map_cache)

    # Save the patterns to a secure file
    save_path = '/home/killswitch/encryption_patterns.json'  # Replace with your secure path to save the patterns
    save_patterns_to_file({'letter_pattern': letter_pattern, 'digit_pattern': digit_pattern}, save_path)


    # Now use letter_pattern_dec and digit_pattern_dec to decrypt the data
   # Decryption demonstration (assume patterns are loaded from a secure location)
    loaded_patterns = load_patterns_from_file(save_path)
    # Decrypt with digit pattern and then with letter pattern, using the caches
    decrypted_key_digits = decrypt_with_pattern_updated(encrypted_key, loaded_patterns['digit_pattern'], False, digit_substitution_map_cache)
    decrypted_key = decrypt_with_pattern_updated(decrypted_key_digits, loaded_patterns['letter_pattern'], True, letter_substitution_map_cache)

    
    # Encrypt the shift patterns using the Vigenère cipher
    keyword = "YOURKEYWORD"  # Replace with your chosen keyword
    vigenere_encrypted_letter_pattern = vigenere_cipher_for_numbers(letter_pattern, keyword)
    vigenere_encrypted_digit_pattern = vigenere_cipher_for_numbers(digit_pattern, keyword)

    # For decryption, first reverse Vigenère cipher on the encrypted patterns
    letter_pattern_dec = inv_vigenere_cipher_for_numbers(vigenere_encrypted_letter_pattern, keyword)
    digit_pattern_dec = inv_vigenere_cipher_for_numbers(vigenere_encrypted_digit_pattern, keyword)


    # Print the Vigenère-encrypted shift patterns
    print(f"Vigenère Encrypted Letter Pattern: {vigenere_encrypted_letter_pattern}")
    print(f"Vigenère Encrypted Digit Pattern: {vigenere_encrypted_digit_pattern}")
   
    # Print results
    print(f"Recovery Key: {recovery_key}")
    print(f"Encrypted Key: {encrypted_key}")
    print(f"Decrypted Key: {decrypted_key}")