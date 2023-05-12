from lark import Lark, Transformer
import argparse


class DumboTemplateEngine(Transformer):
    def __init__(self, variables, grammar):
        self.variables = variables
        self.template_grammar = grammar
        self.output = []

    def text(self, tokens):
        return tokens[0]

    def placeholder(self, tokens):
        placeholder_name = tokens[0]
        return self.variables.get(placeholder_name, "")

    def render(self, template):
        parser = Lark(self.template_grammar, start='programme')
        tree = parser.parse(template)
        self.output = []
        self.traverse_tree(tree)
        return ''.join(self.output)
    
    def traverse_tree(self, node):
        if isinstance(node, str):
            self.output.append(node)
        elif node.data == 'variable':
            variable_name = node.children[0]
            value = self.variables.get(variable_name, '')
            print("Value : " + str(node))
            self.output.append(str(value))
        else:
            for child in node.children:
                self.traverse_tree(child)


def main():
    arg_parser = argparse.ArgumentParser(description='Dumbo programming language')
    
    arg_parser.add_argument('data_file', metavar='data_file', type=str, help='A file containing Dumbo code declaring variables and data')
    arg_parser.add_argument('template_file', metavar='template_file', type=str, help='A file containing text and Dumbo code to inject data into')

    args = arg_parser.parse_args()

    data_file = args.data_file
    template_file = args.template_file

    print(f'Data file: {args.data_file}')
    print(f'Template file: {template_file}')

    with open('grammar.lark', 'r') as f:
        grammar = f.read()

    with open(template_file, 'r') as f:
        template_file_content = f.read()

    variables = {"nom": "Lamlih", "prenom": "Houssam", "cours": ('Maths', 'Info')}
    dumbo_engine = DumboTemplateEngine(variables=variables, grammar=grammar)

    output = dumbo_engine.render(template_file_content)
    with open("output.txt", 'w') as f:
        f.write(str(output))

    print(output)


if __name__ == '__main__':
    main()