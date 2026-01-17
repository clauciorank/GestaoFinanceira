import sys
from app.models.schemas import GastoFinanceiro
from pydantic import ValidationError

def verify_payment_methods():
    print("Verifying payment method restriction...")
    
    # Valid cases
    valid_methods = ["Crédito", "Débito", "Refeição", "Pix"]
    for method in valid_methods:
        try:
            gasto = GastoFinanceiro(
                valor=10.0,
                item="Teste",
                categoria="Alimentação",
                meio_pagamento=method
            )
            print(f"✅ Valid method '{method}' accepted.")
        except ValidationError as e:
            print(f"❌ Valid method '{method}' rejected: {e}")
            sys.exit(1)

    # Invalid case
    invalid_method = "Dinheiro"
    try:
        gasto = GastoFinanceiro(
            valor=10.0,
            item="Teste",
            categoria="Alimentação",
            meio_pagamento=invalid_method
        )
        print(f"❌ Invalid method '{invalid_method}' accepted (should fail).")
        sys.exit(1)
    except ValidationError:
        print(f"✅ Invalid method '{invalid_method}' correctly rejected.")

if __name__ == "__main__":
    verify_payment_methods()
