from lark import Lark
import argparse




def main():
    arg_parser = argparse.ArgumentParser(description='Dumbo programming language')
    
    arg_parser.add_argument('data_file', metavar='data_file', type=str, help='A file containing Dumbo code declaring variables and data')
    arg_parser.add_argument('template_file', metavar='template_file', type=str, help='A file containing text and Dumbo code to inject data into')

    args = arg_parser.parse_args()

    print(f'Data file: {args.data_file}')
    print(f'Template file: {args.template_file}')


if __name__ == '__main__':
    main()