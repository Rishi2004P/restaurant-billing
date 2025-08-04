import sys
print("--- Python Environment Info ---")
print(f"Python executable: {sys.executable}")
print(f"sys.version: {sys.version}")
print("sys.path (where Python looks for modules):")
for p in sys.path:
    print(f"  - {p}")
print("-----------------------------")

try:
    from fpdf import FPDF
    print("\nSUCCESS: fpdf2 imported successfully!")
    # Optional: Check package location
    print(f"fpdf2 package located at: {FPDF.__module__}")
except ModuleNotFoundError as e:
    print(f"\nERROR: ModuleNotFoundError: {e}")
    print("fpdf2 could not be found by the Python interpreter.")
except Exception as e:
    print(f"\nERROR: An unexpected error occurred: {type(e).__name__}: {e}")