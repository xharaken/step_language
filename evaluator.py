#!/usr/bin/env python3

""" Evaluator module. """

from enum import Enum, auto
from tokenizer import Tokenizer, TokenType, DebugInfo
from parser import (Parser, ExpressionType, Expression,
                    StatementType, Statement, Program)
import math
import os
import sys


class ValueType(Enum):
    """ ValueType defines value types.

    NUMBER :           A number type.
                       Example: 100, 123.45
    STRING :           A string type.
                       Example: "abc"
    LIST :             A list type.
                       Example: [1, 2, 3]
    NONE :             A None type.
                       Example: None
    FUNCTION :         A user-defined function type.
                       Example: def function(argument) { ...; }
    BUILTIN_FUNCTION : A bulit-in function type.
                       Example: print, assert, len
    """

    NUMBER = "NUMBER"
    STRING = "STRING"
    LIST = "LIST"
    NONE = "NONE"
    FUNCTION = "FUNCTION"
    BUILTIN_FUNCTION = "BUILTIN_FUNCTION"


class Value:
    """ A Value object represents one value.

    Parameters:
    ----------
    self.type : ValueType
        The ValueType of this object.
    self.data :
        If ValueType is ValueType.NUMBER, it stores the number.
        If ValueType is ValueType.STRING, it stores the string.
        If ValueType is ValueType.LIST, it stores the list of Values.
        If ValueType is ValueType.NONE, it is None.
        If ValueType is ValueType.FUNCTION, it stores the StatementFunction
        that represents the function.
        If ValueType is ValueType.BUILTIN_FUNCTION, it stores a function
        that implements the builtin function.
    """

    def __init__(self, value_type, data = None):
        self.type = value_type
        self.data = data

    def boolean_value(data):
        """ A helper function to create a boolean value. We use 1 to represent
        True and 0 to represent False.
        """
        return (Value(ValueType.NUMBER, 1)
                if data else Value(ValueType.NUMBER, 0))

    def is_number(self):
        return self.type == ValueType.NUMBER

    def is_string(self):
        return self.type == ValueType.STRING

    def is_list(self):
        return self.type == ValueType.LIST

    def is_none(self):
        return self.type == ValueType.NONE

    def is_function(self):
        return self.type == ValueType.FUNCTION

    def is_builtin_function(self):
        return self.type == ValueType.BUILTIN_FUNCTION

    def is_true(self):
        """ Returns whether the Value object is True or not.
        """

        if self.type == ValueType.NUMBER:
            return self.data != 0
        if self.type == ValueType.STRING:
            return self.data != ""
        if self.type == ValueType.LIST:
            return self.data != []
        if self.type == ValueType.NONE:
            return False
        if self.type == ValueType.FUNCTION:
            return True
        if self.type == ValueType.BUILTIN_FUNCTION:
            return True
        assert False, "Should not reach here."

    def is_equal(self, other):
        """ Returns whether the Value object is equal to the `other` Value
        object.
        """

        if (self.type == ValueType.NUMBER and
            other.type == ValueType.NUMBER and
            self.data == other.data):
            return True
        if (self.type == ValueType.STRING and
            other.type == ValueType.STRING and
            self.data == other.data):
            return True
        if (self.type == ValueType.NONE and
            other.type == ValueType.NONE and
            self.data == other.data):
            return True
        if (self.type == ValueType.LIST and
            other.type == ValueType.LIST):
            if len(self.data) != len(other.data):
                return False
            for i in range(len(self.data)):
                # Recursively call is_equal() for each list item.
                # The list is equal to the other list only when all the items
                # in the two lists are equal.
                if not self.data[i].is_equal(other.data[i]):
                    return False
            return True
        if (self.type == ValueType.FUNCTION and
            other.type == ValueType.FUNCTION and
            self.data == other.data):
            return True
        if (self.type == ValueType.BUILTIN_FUNCTION and
            other.type == ValueType.BUILTIN_FUNCTION and
            self.data == other.data):
            return True
        return False

    def to_string(self):
        """ Convert the Value object to a string.
        """

        if self.type == ValueType.NUMBER:
            return str(self.data)
        if self.type == ValueType.STRING:
            return self.data
        if self.type == ValueType.LIST:
            results = []
            for element in self.data:
                # Recursively call to_string() for each list item.
                results.append(element.to_string())
            return "[" + ", ".join(results) + "]"
        if self.type == ValueType.NONE:
            return "None"
        if self.type == ValueType.FUNCTION:
            return "FUNCTION"
        if self.type == ValueType.BULITIN_FUNCTION:
            return "BUILTIN_FUNCTION"
        assert False, "Should not reach here."


class ControlType(Enum):
    """ ControlType defines the result of evaluating one Statement.

    NEXT :     The evaluation should continue to the next Statement.
    BREAK :    The evaluation hit a break Statement.
    CONTINUE : The evaluation hit a continue Statement.
    RETURN :   The evaluation hit a return Statement.
    """

    NEXT = "NEXT"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"


class Evaluator:
    """ Evaluator.

    How to use: You can evaluate a program by passing the Program object
    (i.e., the parse tree) to evaluator.evaluate().

        tokenizer = Tokenizer("program.step")
        parser = Parser()
        program = parser.parse(tokenizer)  # Get a parse tree
        evaluator = Evaluator()
        evaluator.evaluate(program)  # Evaluate the parse tree

    Parameters:
    ----------
    self.__variables : Dictionary from strings to Values.
        A mapping from global variables to values.
    """

    def __init__(self):
        self.__variables = {}
        self.__install_builtin_functions()

    def evaluate(self, program):
        """ Evaluate the parse tree. """

        self.__evaluate_program(program)

    def __evaluate_program(self, program):
        """ Evaluate Program. """

        for s in program.statement_list:
            (control_type, value) = self.__evaluate_statement(s)
            if control_type != ControlType.NEXT:
                raise Exception(
                    "%s was returned to the top level." % control_type.value)

    """ __evaluate_statement*() evaluates a Statement and returns
    (ControlType, Value).

    If ControlType is NEXT, the evaluation should continue to the next
    statement. If ControlType is BREAK, CONTINUE or RETURN, the evaluation hit
    BREAK, CONTINUE or RETURN respectively and should be handled appropriately.
    For example, a while statement should break the evaluation when the current
    statement returns BREAK.

    If ControlType is RETURN and the return statement has a return value,
    the Value is set to the return value. Otherwise, the Value is None.
    """

    def __evaluate_statement(self, statement):
        """ Evaluate Statement. """

        if statement.type == StatementType.NONE:
            return self.__evaluate_statement_none(statement)
        if statement.type == StatementType.EXPRESSION:
            return self.__evaluate_statement_expression(statement)
        if statement.type == StatementType.IF:
            return self.__evaluate_statement_if(statement)
        if statement.type == StatementType.WHILE:
            return self.__evaluate_statement_while(statement)
        if statement.type == StatementType.BREAK:
            return self.__evaluate_statement_break(statement)
        if statement.type == StatementType.CONTINUE:
            return self.__evaluate_statement_continue(statement)
        if statement.type == StatementType.RETURN:
            return self.__evaluate_statement_return(statement)
        if statement.type == StatementType.FUNCTION:
            return self.__evaluate_statement_function(statement)
        assert False, "Should not reach here"

    def __evaluate_statement_expression(self, statement):
        """ Evaluate StatementExpression. """

        value = self.__evaluate_expression(statement.expression)
        return (ControlType.NEXT, value)

    def __evaluate_statement_none(self, statement):
        """ Evaluate StatementNone. """

        return (ControlType.NEXT, None)

    def __evaluate_statement_if(self, statement):
        """ Evaluate StatementIf. """

        value = self.__evaluate_expression(statement.expression)
        if value.is_true():
            return self.__evaluate_statement_list(statement.statement_list1)
        # An else clause may not exist.
        if statement.statement_list2:
            return self.__evaluate_statement_list(statement.statement_list2)
        return (ControlType.NEXT, None)

    def __evaluate_statement_while(self, statement):
        """ Evaluate StatementWhile. """

        while True:
            value = self.__evaluate_expression(statement.expression)
            if not value.is_true():
                break
            (control_type, value) = self.__evaluate_statement_list(
                statement.statement_list1)
            if control_type == ControlType.BREAK:
                break
            if control_type == ControlType.RETURN:
                return (control_type, value)
        return (ControlType.NEXT, None)

    def __evaluate_statement_break(self, statement):
        """ Evaluate StatementBreak. """

        return (ControlType.BREAK, None)

    def __evaluate_statement_continue(self, statement):
        """ Evaluate StatementContinue. """

        return (ControlType.CONTINUE, None)

    def __evaluate_statement_return(self, statement):
        """ Evaluate StatementReturn. """

        value = Value(ValueType.NONE)
        # The return value may not exist.
        if statement.expression:
            value = self.__evaluate_expression(statement.expression)
        return (ControlType.RETURN, value)

    def __evaluate_statement_function(self, statement):
        """ Evaluate StatementFunction. """

        self.__variables[statement.identifier.token.value] = (
            Value(ValueType.FUNCTION, statement))
        return (ControlType.NEXT, None)

    def __evaluate_statement_list(self, statement_list):
        """ A helper function to evaluate a list of Statements. The evaluation
        continues as long as the Statement evaluation returns NEXT. The
        evaluation should return immediately otherwise. """

        for s in statement_list:
            (control_type, value) = self.__evaluate_statement(s)
            if control_type != ControlType.NEXT:
                return (control_type, value)
        return (ControlType.NEXT, None)

    """ __evaluate_expression*() evaluates an Expression and returns the
    result as a Value object.
    """

    def __evaluate_expression(self, expression):
        """ Evaluate Expression. """

        if expression.type == ExpressionType.ASSIGNMENT:
            return self.__evaluate_expression_assignment(expression)
        if expression.type == ExpressionType.ANDOR:
            return self.__evaluate_expression_andor(expression)
        if expression.type == ExpressionType.BINARY:
            return self.__evaluate_expression_binary(expression)
        if expression.type == ExpressionType.UNARY:
            return self.__evaluate_expression_unary(expression)
        if expression.type == ExpressionType.LITERAL:
            return self.__evaluate_expression_value(expression)
        if expression.type == ExpressionType.IDENTIFIER:
            return self.__evaluate_expression_identifier(expression)
        if expression.type == ExpressionType.LIST:
            return self.__evaluate_expression_list(expression)
        if expression.type == ExpressionType.SUBSCRIPTION:
            return self.__evaluate_expression_subscription(expression)
        if expression.type == ExpressionType.CALL:
            return self.__evaluate_expression_call(expression)
        assert False, "Should not reach here."

    def __evaluate_expression_assignment(self, expression):
        """ Evaluate ExpressionAssignment. """

        # identifier = <expression>
        if expression.expression1.type == ExpressionType.IDENTIFIER:
            value = self.__evaluate_expression(expression.expression2)
            self.__variables[expression.expression1.token.value] = value
            return value
        # list[index] = <expression>
        if expression.expression1.type == ExpressionType.SUBSCRIPTION:
            list_value = self.__evaluate_expression(
                expression.expression1.expression1)
            index_value = self.__evaluate_expression(
                expression.expression1.expression2)
            result_value = self.__evaluate_expression(expression.expression2)
            if list_value.is_list() and index_value.is_number():
                if (isinstance(index_value.data, int) and
                    0 <= index_value.data and
                    index_value.data < len(list_value.data)):
                    list_value.data[index_value.data] = result_value
                    return result_value
                expression.debug_info.raise_exception(
                    "Index '%d' is out of range." % index_value.data)
            expression.debug_info.raise_exception(
                "Type error. '%s'['%s'] cannot be evaluated." %
                (list_value.type.value, index_value.type.value))
        expression.debug_info.raise_exception(
            "Invalid assignment. The left side of the assignment must be " +
            "an identifier or a subscription.")

    def __evaluate_expression_andor(self, expression):
        """ Evaluate ExpressionAndOr. """

        if expression.token.type == TokenType.AND:
            value1 = self.__evaluate_expression(expression.expression1)
            # If the first Expression is False, do not evaluate the second
            # Expression.
            if not value1.is_true():
                return Value.boolean_value(False)
            value2 = self.__evaluate_expression(expression.expression2)
            return Value.boolean_value(value2.is_true())
        elif expression.token.type == TokenType.OR:
            value1 = self.__evaluate_expression(expression.expression1)
            # If the first Expression is True, do not evaluate the second
            # Expression.
            if value1.is_true():
                return Value.boolean_value(True)
            value2 = self.__evaluate_expression(expression.expression2)
            return Value.boolean_value(value2.is_true())
        assert False, "Should not reach here."

    def __evaluate_expression_binary(self, expression):
        """ Evaluate ExpressionBinary. """

        value1 = self.__evaluate_expression(expression.expression1)
        value2 = self.__evaluate_expression(expression.expression2)
        if expression.token.type == TokenType.MULTIPLY:
            if value1.is_number() and value2.is_number():
                return Value(ValueType.NUMBER, value1.data * value2.data)
            if value1.is_number() and value2.is_string():
                return Value(ValueType.STRING, value1.data * value2.data)
            if value1.is_string() and value2.is_number():
                return Value(ValueType.STRING, value1.data * value2.data)
            if value1.is_number() and value2.is_list():
                return Value(ValueType.LIST, value1.data * value2.data)
            if value1.is_list() and value2.is_number():
                return Value(ValueType.LIST, value1.data * value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' * '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.DIVIDE:
            if value1.is_number() and value2.is_number():
                return Value(ValueType.NUMBER, value1.data / value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' / '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.MOD:
            if value1.is_number() and value2.is_number():
                return Value(ValueType.NUMBER, value1.data % value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' \% '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.PLUS:
            if value1.is_number() and value2.is_number():
                return Value(ValueType.NUMBER, value1.data + value2.data)
            if value1.is_string() and value2.is_string():
                return Value(ValueType.STRING, value1.data + value2.data)
            if value1.is_list() and value2.is_list():
                return Value(ValueType.LIST, value1.data + value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' + '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.MINUS:
            if value1.is_number() and value2.is_number():
                return Value(ValueType.NUMBER, value1.data - value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' - '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.LT:
            if value1.is_number() and value2.is_number():
                return Value.boolean_value(value1.data < value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' < '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.GT:
            if value1.is_number() and value2.is_number():
                return Value.boolean_value(value1.data > value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' > '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.LE:
            if value1.is_number() and value2.is_number():
                return Value.boolean_value(value1.data <= value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' <= '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.GE:
            if value1.is_number() and value2.is_number():
                return Value.boolean_value(value1.data >= value2.data)
            expression.debug_info.raise_exception(
                "Type error. '%s' >= '%s' cannot be evaluated." %
                (value1.type.value, value2.type.value))
        if expression.token.type == TokenType.EQEQ:
            return Value.boolean_value(value1.is_equal(value2))
        if expression.token.type == TokenType.NOTEQ:
            return Value.boolean_value(not value1.is_equal(value2))
        assert False, "Should not reach here."

    def __evaluate_expression_unary(self, expression):
        """ Evaluate ExpressionUnary. """

        value = self.__evaluate_expression(expression.expression1)
        if expression.token.type == TokenType.MINUS:
            if value.is_number():
                return Value(ValueType.NUMBER, -value.data)
            expression.debug_info.raise_exception(
                "Type error. -'%s' cannot be evaluated" % (value.type.value))
        assert False, "Should not reach here."

    def __evaluate_expression_value(self, expression):
        """ Evaluate ExpressionLiteral. """

        if expression.token.type == TokenType.NUMBER:
            return Value(ValueType.NUMBER, expression.token.value)
        if expression.token.type == TokenType.STRING:
            return Value(ValueType.STRING, expression.token.value)
        if expression.token.type == TokenType.NONE:
            return Value(ValueType.NONE)
        assert False, "Should not reach here."

    def __evaluate_expression_identifier(self, expression):
        """ Evaluate ExpressionIdentifier. """

        if expression.token.type == TokenType.IDENTIFIER:
            if expression.token.value in self.__variables:
                return self.__variables[expression.token.value]
            expression.debug_info.raise_exception(
                "Undefined variable. '%s' is not defined." %
                expression.token.value)
        assert False, "Should not reach here."

    def __evaluate_expression_list(self, expression):
        """ Evaluate ExpressionList. """

        value = []
        for e in expression.expression_list:
            value.append(self.__evaluate_expression(e))
        return Value(ValueType.LIST, value)

    def __evaluate_expression_subscription(self, expression):
        """ Evaluate ExpressionSubscription. """

        value1 = self.__evaluate_expression(expression.expression1)
        value2 = self.__evaluate_expression(expression.expression2)
        if value1.is_list() and value2.is_number():
            if (isinstance(value2.data, int) and
                0 <= value2.data and value2.data < len(value1.data)):
                return value1.data[value2.data]
            expression.debug_info.raise_exception(
                "Index '%d' is out of range." % value2.data)
        if value1.is_string() and value2.is_number():
            if (isinstance(value2.data, int) and
                0 <= value2.data and value2.data < len(value1.data)):
                return Value(ValueType.STRING, value1.data[value2.data])
            expression.debug_info.raise_exception(
                "Index '%d' is out of range." % value2.data)
        expression.debug_info.raise_exception(
            "Type error. '%s'['%s'] cannot be evaluated." %
            (value1.type.value, value2.type.value))

    def __evaluate_expression_call(self, expression):
        """ Evaluate ExpressionCall. """

        function_value = self.__evaluate_expression(expression.expression1)
        arguments = []
        for e in expression.expression_list:
            arguments.append(self.__evaluate_expression(e))
        if function_value.is_builtin_function():
            return function_value.data(arguments, expression.debug_info)
        if function_value.is_function():
            statement = function_value.data
            if len(arguments) != len(statement.argument_list):
                expression.debug_info.raise_exception(
                    "The function '%s' expects %d arguments but " +
                    "%d arguments were provided." % (
                        statement.identifier.token.value,
                        len(statement.argument_list), len(arguments)))
            for i in range(len(arguments)):
                self.__variables[
                    statement.argument_list[i].token.value] = arguments[i]
        for s in statement.statement_list1:
            (control_type, value) = self.__evaluate_statement(s)
            if control_type == ControlType.RETURN:
                return value
            if control_type != ControlType.NEXT:
                raise Exception(
                    "%s was returned while evaluating function '%s'" %
                    (control_type.value, identifier))
        # Return None when the return value is missing.
        return Value(ValueType.NONE);

    def __install_builtin_functions(self):
        """ Install builtin functions.

        Builtin functions take two parameters. The first parameter is
        `arguments`, which is a list of argument Values passed to the builtin
        function. The second parameter is `debug_info`, the DebugInfo object.
        """

        self.__variables["print"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_print)
        self.__variables["assert"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_assert)
        self.__variables["len"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_len)
        self.__variables["int"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_int)
        self.__variables["str"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_str)
        self.__variables["sqrt"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_sqrt)
        self.__variables["append"] = Value(ValueType.BUILTIN_FUNCTION,
            self.__builtin_function_append)

    def __builtin_function_print(self, arguments, debug_info):
        """ print() """

        result = []
        for argument in arguments:
            result.append(argument.to_string())
        print(" ".join(result))
        return Value(ValueType.NONE)

    def __builtin_function_assert(self, arguments, debug_info):
        """ assert() """

        if len(arguments) < 1 or 2 < len(arguments):
            debug_info.raise_exception(
                "assert() takes 1 or 2 arguments but %d arguments provided." %
                len(arguments))
        if not arguments[0].is_true():
            message = "assert FAILED: "
            if len(arguments) == 2:
                message += arguments[1].data
            debug_info.raise_exception(message)
        return Value(ValueType.NONE)

    def __builtin_function_len(self, arguments, debug_info):
        """ len() """

        if len(arguments) != 1:
            debug_info.raise_exception(
                "len() takes 1 argument but %d arguments provided."
                % len(arguments))
        if arguments[0].is_list() or arguments[0].is_string():
            return Value(ValueType.NUMBER, len(arguments[0].data))
        debug_info.raise_exception(
            "TypeError. len('%s') cannot be evaluated." %
            arguments[0].type.value)

    def __builtin_function_int(self, arguments, debug_info):
        """ int() """

        if len(arguments) != 1:
            debug_info.raise_exception(
                "int() takes 1 argument but %d arguments provided."
                % len(arguments))
        if arguments[0].is_number() or arguments[0].is_string():
            return Value(ValueType.NUMBER, int(arguments[0].data))
        debug_info.raise_exception(
            "TypeError. int('%s') cannot be evaluated." %
            arguments[0].type.value)

    def __builtin_function_str(self, arguments, debug_info):
        """ str() """

        if len(arguments) != 1:
            debug_info.raise_exception(
                "str() takes 1 argument but %d arguments provided."
                % len(arguments))
        return Value(ValueType.STRING, arguments[0].to_string())

    def __builtin_function_sqrt(self, arguments, debug_info):
        """ sqrt() """

        if len(arguments) != 1:
            debug_info.raise_exception(
                "sqrt() takes 1 argument but %d arguments provided."
                % len(arguments))
        if arguments[0].is_number():
            return Value(ValueType.NUMBER, math.sqrt(arguments[0].data))
        debug_info.raise_exception(
            "TypeError. sqrt('%s') cannot be evaluated." %
            arguments[0].type.value)

    def __builtin_function_append(self, arguments, debug_info):
        """ append() """

        if len(arguments) != 2:
            debug_info.raise_exception(
                "append() takes 2 arguments but %d arguments provided."
                % len(arguments))
        if arguments[0].is_list():
            arguments[0].data.append(arguments[1])
            return Value(ValueType.NONE)
        debug_info.raise_exception(
            "TypeError. append('%s', ...) cannot be evaluated." %
            arguments[0].type.value)


def main(filename):
    tokenizer = Tokenizer(filename)
    program = Parser().parse(tokenizer)
    Evaluator().evaluate(program)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s filename" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
