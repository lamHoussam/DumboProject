from lark import Lark, Transformer, Tree
import argparse

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

    parser = Lark(grammar, start='programme')

    with open(template_file, 'r') as f:
        template_file_content = f.read()

    output = parser.parse(template_file_content)
    with open("output.txt", 'w') as f:
        f.write(str(output))

    print(output)


if __name__ == '__main__':
    main()