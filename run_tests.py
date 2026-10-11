import os
import unittest


def run_suite():
    fase_atual = input("Insira a fase atual para personalizar o log: ")
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"log_{fase_atual}.txt")

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="test_*.py")

    with open(log_path, "w", encoding="utf-8") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)

    print(f"Testes concluídos! Resultados gravados em: {log_path}")
    print(f"Executados: {result.testsRun} | Falhas: {len(result.failures)} | Erros: {len(result.errors)}")


if __name__ == "__main__":
    run_suite()
