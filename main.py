import tokenize
from io import BytesIO
import ast
import builtins

class SemanticChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.symbol_table = {name: getattr(builtins, name) for name in dir(builtins) if not name.startswith('_')}

    def visit_FunctionDef(self, node):
        # Add function to symbol table
        self.symbol_table[node.name] = node
        # Check arguments
        for arg in node.args.args:
            self.symbol_table[arg.arg] = arg
        # Visit the body of the function
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self.symbol_table:
            self.errors.append(f"Semantic Error: Variable '{node.id}' used before declaration at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id not in self.symbol_table:
            self.errors.append(f"Semantic Error: Function '{node.func.id}' called before declaration at line {node.lineno}")
        self.generic_visit(node)

    def check(self, source_code):
        tree = ast.parse(source_code)
        self.visit(tree)
        return self.errors

# Sample usage

with open('opers.py', 'rb') as f:
    byte_file = f.read()
        
tokens = tokenize.tokenize(BytesIO(byte_file).readline)

reverse_code = tokenize.untokenize(tokens).decode('utf-8')


checker = SemanticChecker()
error = checker.check(byte_file)


parsed = ast.parse(reverse_code)
print(ast.dump(parsed, indent=4))

        