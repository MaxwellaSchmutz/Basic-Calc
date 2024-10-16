from pair import Pair, nil
from operator import add, sub, mul, truediv


# Part 1 - The Interactive Loop
def main():
    print("Welcome to the CS 111 Calculator Interpreter.")

    # Main loop
    while True:
        user_input = input("calc >> ")

        if user_input == "exit":
            break

        try:
            tokens = tokenize(user_input)
            syntax_tree = parse(tokens)
        except ValueError:
            print("Error: Invalid Expression")
            continue

        # Evaluate the expression and print the result
        print(eval(syntax_tree))

    # Farewell message
    print("Goodbye!")


# Part 2 - Parsing the Input


# Task 1 - Getting the Token List
def tokenize(expression):
    """Tokenize the given expression."""
    expression = expression.replace("(", " ( ").replace(')', " ) ")
    return expression.split()


# Task 2 - Creating the Expression Tree
def parse(tokens):
    """Parse the tokenized expression and build the syntax tree."""

    def parse_tokens(tokens, index):
        """Helper function to recursively parse tokens."""
        t, i = tokens, index
        if t[i] == '(':
            op = t[i + 1]
            if i != 0:
                pair, i = parse_tokens(t, i + 2)
                op = Pair(op, pair)
            elif i == 0:
                i += 2
            pair, i = parse_tokens(t, i)
            return Pair(op, pair), i
        elif t[i] == ')':
            return nil, i + 1
        try:
            if '.' in t[i]:
                num = float(t[i])
            else:
                num = int(t[i])
            pair, i = parse_tokens(t, i + 1)
            return Pair(num, pair), i
        except ValueError:
            raise TypeError("Invalid expression")

    try:
        tree, _ = parse_tokens(tokens, 0)
        return tree
    except TypeError:
        raise TypeError("Invalid expression")


# Part 3 - Evaluating the Syntax Tree


# Task 1 - The reduce() Function
def reduce(func, operands, initial):
    # Initialize the result with the initial value
    result = initial

    # Start with a while loop to iterate through the operands
    while operands != nil:  # Loop until we reach the end of the list
        # Get the value of the current pair
        current_value = operands.first
        # Apply the given function to combine it with the current result
        result = func(result, current_value)
        # Move to the next pair in the list
        operands = operands.rest
    # Return the accumulated result
    return result


# Task 2 - Applying the Operators
def apply(operator, operands):
    # Call the appropriate function based on the operator
    if operator == '+':
        return reduce(add, operands, 0)
    elif operator == '-':
        return reduce(sub, operands.rest, operands.first)
    elif operator == '*':
        return reduce(mul, operands, 1)
    elif operator == '/':
        return reduce(truediv, operands.rest, operands.first)
    else:
        raise TypeError("Invalid operator: {}".format(operator))


def eval(syntax_tree):
    if isinstance(syntax_tree, (int, float)):
        return syntax_tree
    elif isinstance(syntax_tree, Pair):
        if isinstance(syntax_tree.first, Pair):  # If the operator is a subexpression
            evaluated_operator = eval(syntax_tree.first)
            evaluated_operands = syntax_tree.rest.map(eval)
            return Pair(evaluated_operator, evaluated_operands)
        elif isinstance(syntax_tree.first, str) and syntax_tree.first in ["+", "-", "*", "/"]:
            # Apply the operator to the evaluated operands
            evaluated_operands = syntax_tree.rest.map(eval)
            return apply(syntax_tree.first, evaluated_operands)
        else:
            raise TypeError("Invalid expression")
    else:
        raise TypeError("Invalid expression")



if __name__ == "__main__":
    main()
