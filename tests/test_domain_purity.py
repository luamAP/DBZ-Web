import ast
import os
import unittest


class ForbiddenCallVisitor(ast.NodeVisitor):
    FORBIDDEN_NAMES = {'print', 'input', 'sleep'}
    FORBIDDEN_ATTRIBUTES = {('time', 'sleep')}

    def __init__(self, filepath):
        self.filepath = filepath
        self.violations = []

    def visit_Call(self, node):
        # Chamada direta: print(...), input(...), sleep(...)
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN_NAMES:
                self.violations.append(
                    f"{self.filepath}:{node.lineno} - Chamada direta proibida: '{node.func.id}()'"
                )
        # Chamada qualificada: time.sleep(...)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                module_name = node.func.value.id
                method_name = node.func.attr
                if (module_name, method_name) in self.FORBIDDEN_ATTRIBUTES:
                    self.violations.append(
                        f"{self.filepath}:{node.lineno} - Chamada qualificada proibida: '{module_name}.{method_name}()'"
                    )

        self.generic_visit(node)


class TestDomainPurity(unittest.TestCase):

    def setUp(self):
        # Determina o diretório base do projeto relativo ao arquivo de teste
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(current_dir)
        self.models_dir = os.path.join(self.project_root, 'models')

    def test_models_directory_has_no_io_or_sleep(self):
        """Garante que nenhum arquivo dentro de models/ utilize print, input ou time.sleep."""
        self.assertTrue(os.path.isdir(self.models_dir), f"Diretório models não encontrado: {self.models_dir}")

        all_violations = []

        for root, _, files in os.walk(self.models_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.project_root)

                    with open(file_path, 'r', encoding='utf-8') as f:
                        source_code = f.read()

                    tree = ast.parse(source_code, filename=rel_path)
                    visitor = ForbiddenCallVisitor(rel_path)
                    visitor.visit(tree)

                    all_violations.extend(visitor.violations)

        if all_violations:
            violations_report = "\n".join(all_violations)
            self.fail(
                f"Violação dos invariantes de arquitetura em models/:\n{violations_report}\n"
                "A camada de domínio deve ser pura e não pode conter print, input ou time.sleep."
            )


if __name__ == '__main__':
    unittest.main()
