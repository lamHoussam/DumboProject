from lark import Lark, Token, Transformer
import argparse


operators = {
    "add_op":"+",
    "sub_op":"-",
    "mul_op":"*",
    "div_op":"/"
}

class DumboTemplateEngine(Transformer):
    def __init__(self, variables, grammar):
        self.variables = variables
        self.template_grammar = grammar
        self.output = []

    def render(self, template):
        parser = Lark(self.template_grammar, start='programme', parser='lalr')
        tree = parser.parse(template)
        self.output = []
        self.traverse_tree(tree)
        return ''.join(self.output)
    
    def evaluate_string_list(self, node):
        all_elements = node.scan_values(lambda v: isinstance(v, Token))
        lst = ','.join(all_elements).split(",")
        return tuple(lst)
        
    
    def evaluate_integer_expression(self, node):
        children_num = len(node.children)
        if children_num == 1:
            child = node.children[0]
            if child.data == 'integer':
                return int(str(child.children[0])) 
            elif child.data == 'variable':
                variable_name = child.children[0]
                return self.variables.get(variable_name)
            else:
                return self.evaluate_integer_expression(child)
        elif children_num == 2:
            coeff = -1 if str(node.children[0]) == '-' else 1
            return coeff * self.evaluate_integer_expression(node.children[1])
        else:
            left_operand = self.evaluate_integer_expression(node.children[0])
            operator = operators.get(str(node.children[1].children[0].data))
            right_operand = self.evaluate_integer_expression(node.children[2])

            op_string = str(left_operand) + str(operator) + str(right_operand)
            result = int(eval(op_string))
            
            return result

    def evaluate_boolean_expression(self, node):
        num_children = len(node.children)
        print("Children : " + str(node.data) + " len : " + str(num_children))
        if num_children == 1:
            child = node.children[0]
            if child.data == 'boolean':
                value = str(child.children[0])
                return value == "true" 
            elif child.data == 'variable':
                variable_name = child.children[0]
                return self.variables.get(variable_name)
            else:
                return self.evaluate_boolean_expression(child)
        elif num_children == 2:
            bool_val = self.evaluate_boolean_expression(node.children[1])
            return not bool_val
        else:
            if node.data == 'integer_comparison':
                evaluation_function = self.evaluate_integer_expression
            else:
                evaluation_function = self.evaluate_boolean_expression

            left_side = evaluation_function(node.children[0])
            op = str(node.children[1])
            if op == '=':
                op = '=='
            right_side = evaluation_function(node.children[2])

            string_expression = str(left_side) + " " + op + " " + str(right_side)
            return bool(eval(string_expression))

    def traverse_tree(self, node):
        if isinstance(node, str):
            self.output.append(node)
        elif node.data == 'string':
            print(node)
            value = node.children[0]
            # For now remove all instances of "'"
            self.output.append(str(value).strip("'"))
        elif node.data == 'for_loop':
            collection_node = node.children[1]
            iter_var_name = str(node.children[0].children[0])
            if collection_node.data == 'variable':
                collection = self.variables.get(collection_node.children[0])
            else:
                collection = self.evaluate_string_list(node.children[1])
            size = len(collection)
            # print("Expression for : " + str(node.children[2]))
            if size != 0:
                i = 0
                self.variables[iter_var_name] = collection[i]
                while (True):
                    self.traverse_tree(node.children[2])
                    i+=1
                    if i >= size:
                        break
                    self.variables[iter_var_name] = collection[i]
                
                del self.variables[iter_var_name]

        elif node.data == 'if_statement':
            print("condition : " + str(node.children[0]))
            condition = self.evaluate_boolean_expression(node.children[0])
            print("if statement : " + str(node.children[1]))
            if condition:
                self.traverse_tree(node.children[1])
        elif node.data == 'boolean_expression':
            result = self.evaluate_boolean_expression(node)
            self.output.append(str(result))
        elif node.data == 'integer_expression':
            result = self.evaluate_integer_expression(node)
            print("Got result : " + str(result))
            self.output.append(str(result))
        elif node.data == 'variable':
            variable_name = node.children[0]
            value = self.variables.get(variable_name)
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

    variables = {"nom": "Lamlih", "prenom": "Houssam", "cours": ('Maths', 'Info'), 'integerValue': 5, 'integ': 10}
    dumbo_engine = DumboTemplateEngine(variables=variables, grammar=grammar)

    output = dumbo_engine.render(template_file_content)
    with open("output.txt", 'w') as f:
        f.write(str(output))

    print(output)


if __name__ == '__main__':
    main()