from lark import Lark, Token, Transformer, UnexpectedToken
import argparse


operators = {
    "add_op":"+",
    "sub_op":"-",
    "mul_op":"*",
    "div_op":"/"
}

class DumboTemplateEngineError(Exception):
    pass

class DumboTemplateEngine(Transformer):
    def __init__(self, grammar):
        self.global_variables = {}
        self.local_variables = {}
        self.template_grammar = grammar
        self.output = []
        self.parser = Lark(self.template_grammar, start='programme', parser='lalr')

    def load_variables_data(self, data):
        try:
            tree = self.parser.parse(data)
            self.traverse_tree(tree, True)
        except UnexpectedToken as e:
            line, column = e.line, e.column
            error_message = f"Syntax error at line {line}, column {column}: {e}"
            raise DumboTemplateEngineError(error_message)


        # print("Variables : " + str(self.global_variables))

    def render(self, template):
        try:
            tree = self.parser.parse(template)
            self.output = []
            self.traverse_tree(tree)
            return ''.join(self.output)
        except UnexpectedToken as e:
            line, column = e.line, e.column
            error_message = f"Syntax error at line {line}, column {column}: {e}"
            raise DumboTemplateEngineError(error_message)
    
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
                value = self.local_variables.get(variable_name)
                if value is None:
                    value = self.global_variables.get(variable_name)
                return value
            else:
                return self.evaluate_integer_expression(child)
        elif children_num == 2:
            coeff = -1 if str(node.children[0]) == '-' else 1
            return int(coeff) * int(self.evaluate_integer_expression(node.children[1]))
        else:
            left_operand = self.evaluate_integer_expression(node.children[0])
            operator = operators.get(str(node.children[1].children[0].data))
            right_operand = self.evaluate_integer_expression(node.children[2])

            op_string = str(left_operand) + str(operator) + str(right_operand)
            result = int(eval(op_string))
            
            return result

    def evaluate_boolean_expression(self, node):
        num_children = len(node.children)
        if num_children == 1:
            child = node.children[0]
            if child.data == 'boolean':
                value = str(child.children[0])
                return value == "true" 
            elif child.data == 'variable':
                variable_name = child.children[0]
                value = self.local_variables.get(variable_name)
                if value is None:
                    value = self.global_variables.get(variable_name)
                return value
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

    def traverse_tree(self, node, loading_data = False):
        if isinstance(node, str):
            self.output.append(node)
        elif node.data == 'string':
            value = node.children[0]
            # For now remove all instances of "'"
            self.output.append(str(value).strip("'"))

        elif node.data == 'assign_statement':
            var_name = ''.join(node.children[0].scan_values(lambda v: isinstance(v, Token)))
            value_node = node.children[1]
            var_value = ','.join(value_node.scan_values(lambda v: isinstance(v, Token)))
            lst = var_value.split(",")

            
            var_value = var_value.strip("'") if len(lst) == 1 else tuple(lst)
            if value_node.data == 'integer_expression':
                var_value = self.evaluate_integer_expression(value_node)

            variables_dict = self.global_variables if loading_data else self.local_variables
            variables_dict[var_name] = var_value
            # print("Variables : " + str(variables_dict))

        elif node.data == 'for_loop':
            collection_node = node.children[1]
            iter_var_name = str(node.children[0].children[0])
            if collection_node.data == 'variable':
                collection = self.local_variables.get(collection_node.children[0])
                if collection is None:
                    collection = self.global_variables.get(collection_node.children[0])
            else:
                collection = self.evaluate_string_list(node.children[1])
                collection = tuple(element.strip("'") for element in collection)
            
            if collection is None:
                return
            size = len(collection)
            # print("Expression for : " + str(node.children[2]))
            if size != 0:
                i = 0
                self.local_variables[iter_var_name] = collection[i]
                while (True):
                    self.traverse_tree(node.children[2], loading_data)
                    i+=1
                    if i >= size:
                        break
                    self.local_variables[iter_var_name] = collection[i]
                
                del self.local_variables[iter_var_name]

        elif node.data == 'if_statement':
            condition = self.evaluate_boolean_expression(node.children[0])
            if condition:
                self.traverse_tree(node.children[1], loading_data)
        elif node.data == 'boolean_expression':
            result = self.evaluate_boolean_expression(node)
            self.output.append(str(result))
        elif node.data == 'integer_expression':
            result = self.evaluate_integer_expression(node)
            self.output.append(str(result))
        elif node.data == 'variable':
            variable_name = node.children[0]
            value = self.local_variables.get(variable_name)
            if value is None:
                value = self.global_variables.get(variable_name)
            self.output.append(str(value))
        else:
            for child in node.children:
                self.traverse_tree(child, loading_data)


def main():
    arg_parser = argparse.ArgumentParser(description='Dumbo Template Engine')
    
    arg_parser.add_argument('data_file', metavar='data_file', type=str, help='A file containing Dumbo code declaring variables and data')
    arg_parser.add_argument('template_file', metavar='template_file', type=str, help='A file containing text and Dumbo code to inject data into')

    args = arg_parser.parse_args()

    data_file = args.data_file
    template_file = args.template_file

    print(f'Data file: {args.data_file}')
    print(f'Template file: {template_file}')

    try:
        with open('grammar.lark', 'r') as f:
            grammar = f.read()

        with open(data_file, 'r') as f:
            data = f.read()

        with open(template_file, 'r') as f:
            template_file_content = f.read()

        dumbo_engine = DumboTemplateEngine(grammar=grammar)

        try:
            dumbo_engine.load_variables_data(data=data)
            output = dumbo_engine.render(template_file_content)
            with open("output.txt", 'w') as f:
                f.write(str(output))
            print(output)
        except DumboTemplateEngineError as e:
            print(f"Dumbo Template engine error: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()