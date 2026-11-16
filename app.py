import os
from dotenv import load_dotenv

load_dotenv()

def get_password():
    password = os.getenv("APP_PASSWORD")
    if not password:
        raise RuntimeError("APP_PASSWORD n'est pas configuré")
    return password


def calculate(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Division par zéro")
        return a / b
    raise ValueError("Opération non autorisée")


def get_message():
    _ = get_password()
    a = float(input("Premier nombre : "))
    b = float(input("Deuxième nombre : "))
    operation = input("Opération (add, subtract, multiply, divide) : ")
    result = calculate(a, b, operation)
    return f"Résultat : {result}"
