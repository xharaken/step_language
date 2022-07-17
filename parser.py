#!/usr/bin/env python3

""" Parser module. """

from enum import Enum, auto
from tokenizer import Tokenizer, TokenType, DebugInfo
import os
import sys


class ExpressionType(Enum):
    """ ExpressionType defines expression types.

    ASSIGNMENT :   An assignment expression.
                   Example: x = 100
    ANDOR :        An expression composed of 'and' or 'or'.
                   Example: x and y, x or y
    BINARY :       An expression composed of binary operators ('*', '/', '%',
                   '+', '-', '<', '>', '<=', '>=', '==' and '!=').
                   Example: x + y, x % y, x == y
    UNARY :        An expression composed of an unary operator ('-').
                   Example: -x
    LITERAL :      A number, a string, or None.
                   Example: 100.0, "abcde", None
    IDENTIFIER :   An identifier.
                   Example: x
    LIST :         A list.
                   Example: [1, 2, 3]
    SUBSCRIPTION : A subscription expression to an item in a list.
                   Example: array[2]
    CALL :         A function call.
                   Example: print(100, 200, 300)
    """

    ASSIGNMENT = "ASSIGNMENT"
    ANDOR = "ANDOR"
    BINARY = "BINARY"
    UNARY = "UNARY"
    LITERAL = "LITERAL"
    IDENTIFIER = "IDENTIFIER"
    LIST = "LIST"
    SUBSCRIPTION = "SUBSCRIPTION"
    CALL = "CALL"


class Expression:
    """ A base class of the Expression classes. Each Expression class uses
    a different set of member variables to store the information about the
    expression. See the comment on each Expression class.
    """

    def __init__(self, expression_type, expression1, expression2,
                 expression_list, token, debug_info):
        self.type = expression_type
        self.expression1 = expression1
        self.expression2 = expression2
        self.expression_list = expression_list
        self.token = token
        self.debug_info = debug_info

    def print(self):
        """ The print() method is overridden by each Expression class. """

        assert False, "Should not reach here"


class ExpressionAssignment(Expression):
    """ An Expression class for ExpressionType.ASSIGNMENT.

        Example: x = 100

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.ASSIGNMENT.
    self.expression1 : Expression
        The left side expression ('x' in the example).
    self.expression2 : Expression
        The right side expression ('100' in the example).
    self.expression_list : None
        Unused.
    self.token : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression1, expression2, debug_info):
        super().__init__(ExpressionType.ASSIGNMENT, expression1, expression2,
                         None, None, debug_info)

    def print(self):
        self.expression1.print()
        print(" = ", end="")
        self.expression2.print()


class ExpressionAndOr(Expression):
    """ An Expression class for ExpressionType.ANDOR.

        Example: x and y

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.ANDOR.
    self.expression1 : Expression
        The left side expression ('x' in the example).
    self.expression2 : Expression
        The right side expression ('y' in the example).
    self.expression_list : None
        Unused.
    self.token : Token
        The operator token. 'and' or 'or'.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression1, expression2, token, debug_info):
        super().__init__(ExpressionType.ANDOR, expression1, expression2,
                         None, token, debug_info)

    def print(self):
        self.expression1.print()
        print(" ", end="")
        self.token.print()
        print(" ", end="")
        self.expression2.print()


class ExpressionBinary(Expression):
    """ An Expression class for ExpressionType.BINARY.

        Example: x + y, x % y, x == y

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.BINARY.
    self.expression1 : Expression
        The left side expression ('x' in the example).
    self.expression2 : Expression
        The right side expression ('y' in the example).
    self.expression_list : None
        Unused.
    self.token : Token
        The operator token. '*', '/', '%', '+', '-', '<', '>', '<=', '>=',
        '==' or '!='.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression1, expression2, token, debug_info):
        super().__init__(ExpressionType.BINARY, expression1, expression2,
                         None, token, debug_info)

    def print(self):
        self.expression1.print()
        print(" ", end="")
        self.token.print()
        print(" ", end="")
        self.expression2.print()


class ExpressionUnary(Expression):
    """ An Expression class for ExpressionType.UNARY.

        Example: -x

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.UNARY.
    self.expression1 : Expression
        The right side expression ('x' in the example).
    self.expression2 : None
        Unused.
    self.expression_list : None
        Unused.
    self.token : Token
        The operator token. '-'.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression1, token, debug_info):
        super().__init__(ExpressionType.UNARY, expression1,
                         None, None, token, debug_info)

    def print(self):
        self.token.print()
        self.expression1.print()


class ExpressionLiteral(Expression):
    """ An Expression class for ExpressionType.LITERAL.

        Example: 100.0, "abcde", None

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.LITERAL.
    self.expression1 : None
        Unused.
    self.expression2 : None
        Unused.
    self.expression_list : None
        Unused.
    self.token : Token
        The token that represents the value (a number, a string or None).
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, token, debug_info):
        super().__init__(ExpressionType.LITERAL, None, None, None,
                         token, debug_info)

    def print(self):
        self.token.print()


class ExpressionIdentifier(Expression):
    """ An Expression class for ExpressionType.IDENTIFIER.

        Example: x

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.IDENTIFIER.
    self.expression1 : None
        Unused.
    self.expression2 : None
        Unused.
    self.expression_list : None
        Unused.
    self.token : Token
        The token that represents the identifier.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, token, debug_info):
        super().__init__(ExpressionType.IDENTIFIER,
                         None, None, None, token, debug_info)

    def print(self):
        self.token.print()


class ExpressionList(Expression):
    """ An Expression class for ExpressionType.LIST.

        Example: [1, 2, 3]

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.LIST.
    self.expression1 : None
        Unused.
    self.expression2 : None
        Unused.
    self.expression_list : list of Expressions
        A list of Expressions.
    self.token : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression_list, debug_info):
        super().__init__(ExpressionType.LIST, None, None,
                         expression_list, None, debug_info)

    def print(self):
        print("[", end="")
        for i in range(len(self.expression_list)):
            if i != 0:
                print(", ", end="")
            self.expression_list[i].print()
        print("]", end="")


class ExpressionSubscription(Expression):
    """ An Expression class for ExpressionType.SUBSCRIPTION.

        Example: array[2]

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.SUBSCRIPTION.
    self.expression1 : Expression
        The expression to specify the list ('array' in the example).
    self.expression2 : Expression
        The expression inside [ ] ('2' in the example).
    self.expression_list : None
        Unused.
    self.token : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression1, expression2, debug_info):
        super().__init__(ExpressionType.SUBSCRIPTION, expression1, expression2,
                         None, None, debug_info)

    def print(self):
        self.expression1.print()
        print("[", end="")
        self.expression2.print()
        print("]", end="")


class ExpressionCall(Expression):
    """ An Expression class for ExpressionType.CALL.

        Example: print(100, 200, 300)

    Parameters:
    ----------
    self.type : ExpressionType
        It is set to ExpressionType.CALL.
    self.expression1 : Expression
        The expression to specify the function ('print' in the example).
    self.expression2 : None
        Unused.
    self.expression_list : list of Expressions
        A list of argument Expressions.
    self.token : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression1, expression_list, debug_info):
        super().__init__(ExpressionType.CALL, expression1, None,
                         expression_list, None, debug_info)

    def print(self):
        self.expression1.print()
        print("(", end="")
        for i in range(len(self.expression_list)):
            if i != 0:
                print(", ", end="")
            self.expression_list[i].print()
        print(")", end="")


class StatementType(Enum):
    """ ExpressionType defines expression types.

    NONE :         An empty statement.
                   Example:
                       ;

    EXPRESSION :   An expression statement.
                   Example:
                       3 + 4 * 5;
                       x = array[2];
                       print(100, 200, 300);

    IF :           An if statement.
                   Example:
                       if (condition) {
                           statement1;
                           statement2;
                       } else {
                           statement3;
                           statement4;
                       }

    WHILE :        A while statement.
                   Example:
                       while (condition) {
                           statement1;
                           statement2;
                       }

    BREAK :        A break statement.
                   Example:
                       break;

    CONTINUE :     A continue statement.
                   Example:
                       continue;

    RETURN :       A return statement.
                   Example:
                       return;
                       return 100;
                       return ["abc", "def"];

    FUNCTION :     A def statement to define a function.
                   Example:
                       def function(argument1, argumente2) {
                           statement1;
                           statement2;
                       }
    """

    NONE = "NONE"
    EXPRESSION = "EXPRESSION"
    IF = "IF"
    WHILE = "WHILE"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"
    FUNCTION = "FUNCTION"


class Statement:
    """ A base class of the Statememnt classes. Each Statement class uses
    a different set of member variables to store the information about the
    statement. See the comment on each Statement class.
    """

    def __init__(self, statement_type, expression, statement_list1,
                 statement_list2, identifier, argument_list):
        self.type = statement_type
        self.expression = expression
        self.statement_list1 = statement_list1
        self.statement_list2 = statement_list2
        self.identifier = identifier
        self.argument_list = argument_list

    def print(self, indent):
        """ The print() method is overridden by each Statement class.
        `indent` specifies how many whitespaces should be printed before
        the statement.
        """

        assert False, "Should not reach here"


class StatementNone(Statement):
    """ An Statement class for StatementType.NONE.

        Example:
            ;

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.NONE.
    self.expression : None
        Unused.
    self.statement_list1 : None
        Unused.
    self.statement_list2 : None
        Unused.
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self):
        super().__init__(StatementType.NONE, None, None, None, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        print(";")


class StatementExpression(Statement):
    """ An Statement class for StatementType.EXPRESSION.

        Example:
            3 + 4 * 5;
            x = array[2];
            print(100, 200, 300);

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.EXPRESSION.
    self.expression : Expression
        The expression of the statement ('3 + 4 * 5' in the first example).
    self.statement_list1 : None
        Unused.
    self.statement_list2 : None
        Unused.
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression):
        super().__init__(StatementType.EXPRESSION, expression,
                         None, None, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        self.expression.print()
        print(";")


class StatementIf(Statement):
    """ An Statement class for StatementType.IF.

        Example:
            if (condition) {
                statement1;
                statement2;
            } else {
                statement3;
                statement4;
            }

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.IF.
    self.expression : Expression
        The condition expression of the if statement.
    self.statement_list1 : list of Statements
        A list of Statements in the if clause ('statement1' and
        'statement2' in the example).
    self.statement_list2 : list of Statements
        A list of Statements in the else clause ('statement3' and
        'statement4' in the example).
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression, statement_list1, statement_list2):
        super().__init__(StatementType.IF, expression,
                         statement_list1, statement_list2, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        print("if (", end="")
        self.expression.print()
        print(") {")
        for statement in self.statement_list1:
            statement.print(indent + 4)
        if self.statement_list2:
            print(" " * indent, end="")
            print("} else {")
            for statement in self.statement_list2:
                statement.print(indent + 4)
        print(" " * indent, end="")
        print("}")


class StatementWhile(Statement):
    """ An Statement class for StatementType.WHILE.

        Example:
            while (condition) {
                statement1;
                statement2;
            }

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.WHILE.
    self.expression : Expression
        The condition expression of the while statement.
    self.statement_list1 : list of Statements
        A list of Statements in the if clause ('statement1' and
        'statement2' in the example).
    self.statement_list2 : None
        Unused.
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression, statement_list1):
        super().__init__(StatementType.WHILE, expression,
                         statement_list1, None, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        print("while (", end="")
        self.expression.print()
        print(") {")
        for statement in self.statement_list1:
            statement.print(indent + 4)
        print(" " * indent, end="")
        print("}")


class StatementBreak(Statement):
    """ An Statement class for StatementType.BREAK.

        Example:
            break;

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.BREAK.
    self.expression : None
        Unused.
    self.statement_list1 : None
        Unused.
    self.statement_list2 : None
        Unused.
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self):
        super().__init__(StatementType.BREAK, None, None, None, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        print("break;")


class StatementContinue(Statement):
    """ An Statement class for StatementType.CONTINUE.

        Example:
            continue;

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.CONTINUE.
    self.expression : None
        Unused.
    self.statement_list1 : None
        Unused.
    self.statement_list2 : None
        Unused.
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self):
        super().__init__(StatementType.CONTINUE, None, None, None, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        print("continue;")


class StatementReturn(Statement):
    """ An Statement class for StatementType.RETURN.

        Example:
            return;
            return 100;
            return ["abc", "def"];

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.RETURN.
    self.expression : Expression
        The expression of the return value. It is None if the return value is
        not specified.
    self.statement_list1 : None
        Unused.
    self.statement_list2 : None
        Unused.
    self.identifier : None
        Unused.
    self.argument_list : None
        Unused.
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, expression):
        super().__init__(StatementType.RETURN, expression,
                         None, None, None, None)

    def print(self, indent):
        print(" " * indent, end="")
        print("return", end="")
        if self.expression:
            print(" ", end="")
            self.expression.print()
        print(";")


class StatementFunction(Statement):
    """ An Statement class for StatementType.FUNCTION.

        Example:
            def function(argument1, argumente2) {
                statement1;
                statement2;
            }

    Parameters:
    ----------
    self.type : StatementType
        It is set to StatementType.FUNCTION.
    self.expression : None
        Unused.
    self.statement_list1 : list of Statements
        A list of Statements in the function ('statement1' and 'statement2'
        in the example).
    self.statement_list2 : None
        Unused.
    self.identifier : Expression
        The Expression of the function identifier ('function' in the example).
    self.argument_list : list of Expressions
        A list of Expressions of the argument identifiers ('argument1' and
        'argument2' in the example).
    self.debug_info : DebugInfo
        A DebugInfo object.
    """

    def __init__(self, identifier, argument_list, statement_list1):
        super().__init__(StatementType.FUNCTION, None,
                         statement_list1, None, identifier, argument_list)

    def print(self, indent):
        print(" " * indent, end="")
        print("def ", end="")
        self.identifier.print()
        print("(", end="")
        for i in range(len(self.argument_list)):
            if i != 0:
                print(", ", end="")
            self.argument_list[i].print()
        print(") {")
        for statement in self.statement_list1:
            statement.print(indent + 4)
        print(" " * indent, end="")
        print("}")


class Program:
    """ A Program class. A Program consists of a list of Statements and is
    the root node of the parse tree.

        Example:
            i = 0;
            while (i < 10) {
                print(i);
                i = i + 1;
            }

    Parameters:
    ----------
    self.statement_list : list of Statements
        A list of Statements in the program.
    """
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def print(self):
        for statement in self.statement_list:
            statement.print(0)


class Parser:
    """ Parser.

    How to use: You can parse a program by giving a Tokenizer to
    parser.parse(). parser.parse() returns the parse tree as a Program object.
    You can print the parse tree by calling program.print().

        tokenizer = Tokenizer("program.step")
        parser = Parser()
        program = parser.parse(tokenizer)  # Get the parse tree.
        program.print()  # Print the parse tree.

    Parameters:
    ----------
    self.__tokenizer: Tokenizer
        The associated Tokenizer.
    self.__current_token: Token
        The token that is being read by the Tokenizer.
    """

    def __init__(self):
        self.__tokenizer = None
        self.__current_token = None

    def parse(self, tokenizer):
        """ Parse the program and return the parse tree as a Program object.
        """

        self.__tokenizer = tokenizer
        self.__current_token = self.__tokenizer.read_token()
        return self.__parse_program()

    def __parse_program(self):
        """
        program ::= statement*
        """

        statement_list = []
        while self.__current_token:
            statement = self.__parse_statement()
            if statement:
                statement_list.append(statement)
        return Program(statement_list)

    def __parse_statement(self):
        """
        statement ::= statement_none | statement_expression | statement_if |
                      statement_while | statement_break | statement_continue |
                      statement_return | statement_function
        """

        if self.__is_current_token(TokenType.SEMICOLON):
            return self.__parse_statement_none()
        if self.__is_current_token(TokenType.IF):
            return self.__parse_statement_if()
        if self.__is_current_token(TokenType.WHILE):
            return self.__parse_statement_while()
        if self.__is_current_token(TokenType.BREAK):
            return self.__parse_statement_break()
        if self.__is_current_token(TokenType.CONTINUE):
            return self.__parse_statement_continue()
        if self.__is_current_token(TokenType.RETURN):
            return self.__parse_statement_return()
        if self.__is_current_token(TokenType.DEF):
            return self.__parse_statement_function()
        return self.__parse_statement_expression()

    def __parse_statement_none(self):
        """
        statement_none ::= ';'
        """

        self.__read_token(TokenType.SEMICOLON)
        return StatementNone()

    def __parse_statement_if(self):
        """
        statement_if ::= 'if' '(' expression ')' '{' statement* '}'
                         [ 'else' '{' statement* '}' ]
        """

        self.__read_token(TokenType.IF)
        self.__read_token(TokenType.LEFT_PARENTHESIS)
        expression = self.__parse_expression()
        self.__read_token(TokenType.RIGHT_PARENTHESIS)
        statement_list1 = self.__parse_statement_list()
        statement_list2 = None
        if self.__is_current_token(TokenType.ELSE):
            self.__read_token(TokenType.ELSE)
            statement_list2 = self.__parse_statement_list()
        return StatementIf(expression, statement_list1, statement_list2)

    def __parse_statement_while(self):
        """
        statement_while ::= 'while' '(' expression ')' '{' statement* '}'
        """

        self.__read_token(TokenType.WHILE)
        self.__read_token(TokenType.LEFT_PARENTHESIS)
        expression = self.__parse_expression()
        self.__read_token(TokenType.RIGHT_PARENTHESIS)
        statement_list = self.__parse_statement_list()
        return StatementWhile(expression, statement_list)

    def __parse_statement_break(self):
        """
        statement_break ::= 'break' ';'
        """

        self.__read_token(TokenType.BREAK)
        self.__read_token(TokenType.SEMICOLON)
        return StatementBreak()

    def __parse_statement_continue(self):
        """
        statement_continue ::= 'continue' ';'
        """

        self.__read_token(TokenType.CONTINUE)
        self.__read_token(TokenType.SEMICOLON)
        return StatementContinue()

    def __parse_statement_return(self):
        """
        statement_return ::= 'return' [ expression ] ';'
        """

        self.__read_token(TokenType.RETURN)
        expression = None
        if not self.__is_current_token(TokenType.SEMICOLON):
            expression = self.__parse_expression()
        self.__read_token(TokenType.SEMICOLON)
        return StatementReturn(expression)

    def __parse_statement_function(self):
        """
        statement_function ::= 'def' expression_identifier '('
                               [ expression_identifier
                               ( ',' expression_identifier )* ] ')'
                               '{' statement* '}'
        """

        self.__read_token(TokenType.DEF)
        identifier = self.__parse_expression_identifier()
        self.__read_token(TokenType.LEFT_PARENTHESIS)
        argument_list = []
        if not self.__is_current_token(TokenType.RIGHT_PARENTHESIS):
            argument = self.__parse_expression_identifier()
            argument_list.append(argument)
        while not self.__is_current_token(TokenType.RIGHT_PARENTHESIS):
            self.__read_token(TokenType.COMMA)
            argument = self.__parse_expression_identifier()
            argument_list.append(argument)
        self.__read_token(TokenType.RIGHT_PARENTHESIS)
        statement_list = self.__parse_statement_list()
        return StatementFunction(identifier, argument_list, statement_list)

    def __parse_statement_expression(self):
        """
        statement_expression ::= expression ';'
        """

        expression = self.__parse_expression()
        self.__read_token(TokenType.SEMICOLON)
        return StatementExpression(expression)

    def __parse_expression(self):
        """
        expression ::= expression_assignment
        """

        return self.__parse_expression_assignment()

    def __parse_expression_assignment(self):
        """
        expression_assignment ::= expression_andor [ ( '=' expression_andor ) ]
        """

        expression1 = self.__parse_expression_andor()
        if self.__is_current_token(TokenType.EQ):
            self.__read_token(TokenType.EQ)
            expression2 = self.__parse_expression_andor()
            expression1 = ExpressionAssignment(expression1, expression2,
                                               DebugInfo(self.__tokenizer))
        return expression1

    def __parse_expression_andor(self):
        """
        expression_andor ::= expression_compare (
                             ( 'and' | 'or' ) expression_compare )*
        """

        expression1 = self.__parse_expression_compare()
        while True:
            token_type = self.__current_token.type
            if (token_type == TokenType.AND or
                token_type == TokenType.OR):
                token = self.__read_token(token_type)
                expression2 = self.__parse_expression_compare()
                expression1 = ExpressionAndOr(
                    expression1, expression2, token,
                    DebugInfo(self.__tokenizer))
            else:
                break
        return expression1

    def __parse_expression_compare(self):
        """
        expression_compare ::= expression_plus [
                               ( '<' | '>' | '<=' | '>=' | '==' | '!=' )
                               expression_plus ]
        """

        expression1 = self.__parse_expression_plus()
        token_type = self.__current_token.type
        if (token_type == TokenType.LT or
            token_type == TokenType.GT or
            token_type == TokenType.LE or
            token_type == TokenType.GE or
            token_type == TokenType.EQEQ or
            token_type == TokenType.NOTEQ):
            token = self.__read_token(token_type)
            expression2 = self.__parse_expression_plus()
            expression1 = ExpressionBinary(
                expression1, expression2, token, DebugInfo(self.__tokenizer))
        return expression1

    def __parse_expression_plus(self):
        """
        expression_plus ::= expression_multiply (
                            ( '+' | '-' ) expression_multiply )*
        """

        expression1 = self.__parse_expression_multiply()
        while True:
            token_type = self.__current_token.type
            if (token_type == TokenType.PLUS or
                token_type == TokenType.MINUS):
                token = self.__read_token(token_type)
                expression2 = self.__parse_expression_multiply()
                expression1 = ExpressionBinary(
                    expression1, expression2, token,
                    DebugInfo(self.__tokenizer))
            else:
                break
        return expression1

    def __parse_expression_multiply(self):
        """
        expression_multiply ::= expression_unary (
                                ( '*' | '/' | '%' ) expression_unary )*
        """

        expression1 = self.__parse_expression_unary()
        while True:
            token_type = self.__current_token.type
            if (token_type == TokenType.MULTIPLY or
                token_type == TokenType.DIVIDE or
                token_type == TokenType.MOD):
                token = self.__read_token(token_type)
                expression2 = self.__parse_expression_unary()
                expression1 = ExpressionBinary(
                    expression1, expression2, token,
                    DebugInfo(self.__tokenizer))
            else:
                break
        return expression1

    def __parse_expression_unary(self):
        """
        expression_unary ::= expression_primary | '-' expression_unary
        """

        if self.__current_token.type == TokenType.MINUS:
            token = self.__read_token(TokenType.MINUS)
            expression = self.__parse_expression_unary()
            return ExpressionUnary(
                expression, token, DebugInfo(self.__tokenizer))
        return self.__parse_expression_primary()

    def __parse_expression_primary(self):
        """
        expression_primary ::= expression_atom ( '[' expression ']' |
                               '(' [ expression ( ',' expression )* ] ')' )*
        """

        expression1 = self.__parse_expression_atom()
        while True:
            if self.__is_current_token(TokenType.LEFT_BRACKET):
                self.__read_token(TokenType.LEFT_BRACKET)
                expression2 = self.__parse_expression()
                self.__read_token(TokenType.RIGHT_BRACKET)
                expression1 = ExpressionSubscription(
                    expression1, expression2, DebugInfo(self.__tokenizer))
            elif self.__is_current_token(TokenType.LEFT_PARENTHESIS):
                self.__read_token(TokenType.LEFT_PARENTHESIS)
                argument_list = []
                if not self.__is_current_token(TokenType.RIGHT_PARENTHESIS):
                    argument = self.__parse_expression()
                    argument_list.append(argument)
                while not self.__is_current_token(TokenType.RIGHT_PARENTHESIS):
                    self.__read_token(TokenType.COMMA)
                    argument = self.__parse_expression()
                    argument_list.append(argument)
                self.__read_token(TokenType.RIGHT_PARENTHESIS)
                expression1 = ExpressionCall(
                    expression1, argument_list, DebugInfo(self.__tokenizer))
            else:
                break
        return expression1

    def __parse_expression_atom(self):
        """
        expression_atom ::= expression_identifier | expression_number |
                            expression_string | expression_none |
                            expression_list | expression_parenthesis
        """

        if self.__is_current_token(TokenType.NUMBER):
            return self.__parse_expression_number()
        if self.__is_current_token(TokenType.STRING):
            return self.__parse_expression_string()
        if self.__is_current_token(TokenType.NONE):
            return self.__parse_expression_none()
        if self.__is_current_token(TokenType.LEFT_BRACKET):
            return self.__parse_expression_list()
        if self.__is_current_token(TokenType.LEFT_PARENTHESIS):
            return self.__parse_expression_parenthesis()
        return self.__parse_expression_identifier()

    def __parse_expression_identifier(self):
        """
        expression_identifier ::= TOKEN_IDENTIFIER
        """

        token = self.__read_token(TokenType.IDENTIFIER)
        return ExpressionIdentifier(token, DebugInfo(self.__tokenizer))

    def __parse_expression_number(self):
        """
        expression_number ::= TOKEN_NUMBER
        """

        token = self.__read_token(TokenType.NUMBER)
        return ExpressionLiteral(token, DebugInfo(self.__tokenizer))

    def __parse_expression_string(self):
        """
        expression_string ::= TOKEN_STRING
        """

        token = self.__read_token(TokenType.STRING)
        return ExpressionLiteral(token, DebugInfo(self.__tokenizer))

    def __parse_expression_none(self):
        """
        expression_none ::= TOKEN_NONE
        """

        token = self.__read_token(TokenType.NONE)
        return ExpressionLiteral(token, DebugInfo(self.__tokenizer))

    def __parse_expression_list(self):
        """
        expression_list ::= '[' [ expression ( ',' expression )* ] ']'
        """

        self.__read_token(TokenType.LEFT_BRACKET)
        expression_list = []
        if not self.__is_current_token(TokenType.RIGHT_BRACKET):
            expression = self.__parse_expression()
            expression_list.append(expression)
        while not self.__is_current_token(TokenType.RIGHT_BRACKET):
            self.__read_token(TokenType.COMMA)
            expression = self.__parse_expression()
            expression_list.append(expression)
        self.__read_token(TokenType.RIGHT_BRACKET)
        return ExpressionList(expression_list, DebugInfo(self.__tokenizer))

    def __parse_expression_parenthesis(self):
        """
        expression_parenthesis ::= '(' expression ')'
        """

        self.__read_token(TokenType.LEFT_PARENTHESIS)
        expression = self.__parse_expression()
        self.__read_token(TokenType.RIGHT_PARENTHESIS)
        return expression

    def __parse_statement_list(self):
        """ A helper function to parse '{' statements* '}'. """

        self.__read_token(TokenType.LEFT_BRACE)
        statement_list = []
        while not self.__is_current_token(TokenType.RIGHT_BRACE):
            statement = self.__parse_statement()
            if statement:
                statement_list.append(statement)
        self.__read_token(TokenType.RIGHT_BRACE)
        return statement_list

    def __is_current_token(self, token_type):
        """ A helper function to check the current token type. """

        return self.__current_token.type == token_type

    def __read_token(self, token_type):
        """ A helper function to read the next token. The function raises
        an exception if the previous token type is not `token_type`. The
        function sets the next token to self.__current_token and returns
        the previous token.
        """

        if self.__current_token.type != token_type:
            DebugInfo(self.__tokenizer).raise_exception(
                "Unexpected token found. " +
                "We were expecting '%s' but found '%s'." %
                (token_type.value, self.__current_token.type.value))
        previous_token = self.__current_token
        self.__current_token = self.__tokenizer.read_token()
        return previous_token


def main(filename):
    tokenizer = Tokenizer(filename)
    program = Parser().parse(tokenizer)
    program.print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s filename" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
