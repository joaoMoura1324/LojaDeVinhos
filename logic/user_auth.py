import re

def validate_email(email):
    """
    Verifica se o email segue o formato padrão.

    O formato válido é: `nome@dominio.extensao`.

    Args:
        email (str): O email a ser validado.

    Returns:
        bool: True se o email for válido, False caso contrário.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_name(name):
    """
    Verifica se o nome contém apenas letras e tem no mínimo 4 caracteres.

    Args:
        name (str): O nome a ser validado.

    Returns:
        bool: True se o nome for válido, False caso contrário.
    """
    return name.isalpha() and len(name) >= 4

def validate_username(username):
    """
    Verifica se o nome de utilizador contém no mínimo 4 caracteres.

    Args:
        username (str): O nome de utilizador a ser validado.

    Returns:
        bool: True se o nome de utilizador for válido, False caso contrário.
    """
    return len(username) >= 4

def validate_password(password):
    """
    Verifica se a senha contém pelo menos 6 caracteres.

    Args:
        password (str): A senha a ser validada.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    return len(password) >= 6

def validate_address(address):
    """
    Verifica se o endereço não está vazio.

    Args:
        address (str): O endereço a ser validado.

    Returns:
        bool: True se o endereço for válido, False caso contrário.
    """
    return bool(address and address.strip())

def validate_user_data(name, username, email, password, address):
    """
    Valida todas as informações do utilizador.

    Verifica se:
        - O nome contém apenas letras e tem no mínimo 4 caracteres.
        - O nome de utilizador tem no mínimo 4 caracteres.
        - O email segue o formato padrão.
        - A senha contém pelo menos 6 caracteres.
        - O endereço não está vazio.

    Args:
        name (str): O nome do utilizador.
        username (str): O nome de utilizador.
        email (str): O email do utilizador.
        password (str): A senha do utilizador.
        address (str): O endereço do utilizador.

    Returns:
        list: Uma lista de mensagens de erro, ou None se todos os dados forem válidos.
    """
    errors = []

    if not validate_name(name):
        errors.append("O nome deve conter apenas letras e ter no mínimo 4 caracteres.")
    if not validate_username(username):
        errors.append("O nome de utilizador deve ter no mínimo 4 caracteres.")
    if not validate_email(email):
        errors.append("O email fornecido não é válido.")
    if not validate_password(password):
        errors.append("A senha deve conter pelo menos 6 caracteres.")
    if not validate_address(address):
        errors.append("O endereço não pode estar vazio.")

    return errors if errors else None
