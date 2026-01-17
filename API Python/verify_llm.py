import sys
from app.services.llm_service import LLMService

def verify_llm_extraction():
    print("Verifying LLM extraction...")
    service = LLMService()
    
    # Test case 1: Text with payment method
    text1 = "Gastei 50 reais com almoço no crédito"
    print(f"\nProcessing: '{text1}'")
    try:
        result1 = service.processar(text1)
        print(f"Result: {result1}")
        
        if result1.get("meio_pagamento") in ["Crédito", "Cartão de Crédito"]:
             print("✅ Payment method extracted correctly.")
        else:
             print(f"⚠️ Payment method extraction might have failed or is different: {result1.get('meio_pagamento')}")
             
    except Exception as e:
        print(f"❌ Error processing text: {e}")

    # Test case 2: Text without payment method
    text2 = "Comprei um café por 5 reais"
    print(f"\nProcessing: '{text2}'")
    try:
        result2 = service.processar(text2)
        print(f"Result: {result2}")
        
        if result2.get("meio_pagamento") is None:
             print("✅ Payment method correctly identified as None.")
        else:
             print(f"⚠️ Payment method should be None but got: {result2.get('meio_pagamento')}")

    except Exception as e:
        print(f"❌ Error processing text: {e}")

if __name__ == "__main__":
    # Note: This requires the LLM service to be functional (API key or local model)
    # If not configured, this might fail or need mocking.
    # Assuming the environment is set up as per previous context.
    try:
        verify_llm_extraction()
    except Exception as e:
        print(f"Verification failed: {e}")
