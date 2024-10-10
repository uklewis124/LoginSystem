def encrypt_password(password):
    # For every character in the password
    # Get the ASCII value of the character
    # The first characters value goes up one
    # The second goes down one
    # And so on
    
    # Convert the ASCII value to a character
    # Concatenate all the characters together
    # Return the encrypted password
    
    # DISCLAIMER: Don't put any real passwords into this program (as it is open source,
    #             and anyone can decrypt the passwords). I AM NOT RESPONSIBLE FOR ANY
    #             DATA LEAKS OR DAMAGE CAUSED BY THIS PROGRAM.
    
    # README:     Change the encryption method BEFORE publishing the program for production.
    #             This file should ALWAYS be kept top secret. If you leak this file, users
    #             can see exactly how their passwords are encrypted, and can decrypt them.
    #             (This will be a huge security risk).
    
    
    encrypted_password = ""
    
    for letter in password:
        ascii_value = ord(letter)
        if ascii_value % 2 == 0:
            encrypted_password += chr(ascii_value + 8)
        else:
            encrypted_password += chr(ascii_value - 5)
    
    del password
    return encrypted_password
