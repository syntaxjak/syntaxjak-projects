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

# Functions to encrypt and decrypt with given patterns
def encrypt_with_pattern(data, pattern, is_letter):
    result = []
    for i, char in enumerate(data):
        if (char.isalpha() if is_letter else char.isdigit()):
            shift = pattern[i % len(pattern)]
            substitution_map = create_substitution_maps(shift, 26 if is_letter else 10, is_letter)
            new_char = substitution_map[char.upper() if is_letter else char]
            result.append(new_char.lower() if char.islower() else new_char)
        else:
            result.append(char)
    return ''.join(result)

def decrypt_with_pattern(data, pattern, is_letter):
    result = []
    for i, char in enumerate(data):
        if (char.isalpha() if is_letter else char.isdigit()):
            shift = pattern[i % len(pattern)]
            substitution_map = create_substitution_maps(-shift, 26 if is_letter else 10, is_letter)
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

# Main script execution
if __name__ == "__main__":
    # Specify the maximum length of the recovery keys
    max_length = 160

    # Generate random patterns for letters and digits
    letter_pattern = generate_random_pattern(max_length, 26)  # Alphabet has 26 letters
    digit_pattern = generate_random_pattern(max_length, 10)   # Digits range from 0 to 9

    # Encryption demonstration
    recovery_key = "ExampleRecoveryKey1-2-3-4-5"  # Replace with your actual key
    encrypted_key = encrypt_with_pattern(recovery_key, letter_pattern, True)
    encrypted_key = encrypt_with_pattern(encrypted_key, digit_pattern, False)

    # Save the patterns to a secure file
    save_path = '/home/killswitch/encryption_patterns.json'  # Replace with your secure path to save the patterns
    save_patterns_to_file({'letter_pattern': letter_pattern, 'digit_pattern': digit_pattern}, save_path)

    # Decryption demonstration (assume patterns are loaded from a secure location)
    loaded_patterns = load_patterns_from_file(save_path)
    decrypted_key = decrypt_with_pattern(encrypted_key, loaded_patterns['digit_pattern'], False)
    decrypted_key = decrypt_with_pattern(decrypted_key, loaded_patterns['letter_pattern'], True)

    # Print results
    print(f"Recovery Key: {recovery_key}")
    print(f"Encrypted Key: {encrypted_key}")
    print(f"Decrypted Key: {decrypted_key}")