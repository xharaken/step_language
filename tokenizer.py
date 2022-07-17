#!/usr/bin/env python3

""" Tokenizer module. """

from enum import Enum, auto
import os
import sys


class TokenType(Enum):
    """ TokenType defines all valid token types. See tokens.txt for the token
    definition. """

    NUMBER = "number"
    IDENTIFIER = "identifier"
    STRING = "string"
    LEFT_PARENTHESIS = "("
    RIGHT_PARENTHESIS = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    MULTIPLY = "*"
    DIVIDE = "/"
    MOD = "%"
    PLUS = "+"
    MINUS = "-"
    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    EQEQ = "=="
    NOTEQ = "!="
    EQ = "="
    COMMA = ","
    SEMICOLON = ";"
    AND = "and"
    OR = "or"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    BREAK = "break"
    CONTINUE = "continue"
    RETURN = "return"
    DEF = "def"
    NONE = "None"


class Token:
    """ A Token object represents one token.

    Parameters:
    ----------
    self.type : TokenType
        The type of the token.
    self.value :
        If self.type is TokenType.NUMBER, self.value stores the number (int or
        float).
        If self.type is TokenType.STRING, self.value stores the string.
        If self.type is TokenType.IDENTIFIER, self.value stores a string of the
        identifier.
        Otherwise, self.value is None.
    """

    def __init__(self, token_type, value = None):
        self.type = token_type
        self.value = value

    def print(self):
        """ Print the token. """

        if self.type == TokenType.NUMBER:
            print(self.value, end="")
        elif self.type == TokenType.STRING:
            print('"' + self.value + '"', end="")
        elif self.type == TokenType.IDENTIFIER:
            print(self.value, end="")
        else:
            print(self.type.value, end="")


class DebugInfo:
    """ DebugInfo is used to raise an exception with useful debug information.

    How to use: You create DebugInfo by passing the tokenizer:

        debug_info = DebugInfo(tokenizer)

    The DebugInfo remembers the current line number and other useful debug
    information. Later you can call:

        debug_info.raise_exception("message")

    This raises an exception with the message, the line number and the source
    code of the line.

    Parameters:
    ----------
    self.tokenizer : Tokenizer
        The tokenizer.
    self.line_start_index : int
        The source code index that starts the current line.
        self.tokenizer.source[self.line_start_index] gives the first character
        of the current line.
    self.line_number : int
        The current line number.
    """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.line_start_index = tokenizer.line_start_index
        self.line_number = tokenizer.line_number

    def raise_exception(self, message):
        """ Raise an exception with useful debug information. """

        line_end = self.tokenizer.source.find('\n', self.line_start_index)
        raise Exception(
            "%s\nline %d: %s" %
            (message, self.line_number,
             self.tokenizer.source[
                 self.line_start_index :
                 (self.tokenizer.__source_length
                  if line_end == -1 else line_end)]))


class Tokenizer:
    """ Tokenizer.

    How to use: You can create a Tokenizer by giving a program filename:

        tokenizer = Tokenizer("program.step")

    tokenizer.read_token() reads one Token and returns the Token. When the
    tokenizer reaches the end of the file, it returns None.

        while token := tokenizer.read_token():
            token.print()  # Print the Token.

    Parameters:
    ----------
    self.source : string
        The source code.
    self.__source_length : int
        The length of the source code.
    self.__index : int
        The current index the tokenizer is reading.
    self.line_start_index : int
        The index that starts the current line.
    self.line_number : int
        The current line number.
    """

    def __init__(self, filename):
        with open(filename) as file:
            self.source = "".join(file.readlines())
            self.__source_length = len(self.source)
        self.__index = 0
        self.line_start_index = 0
        self.line_number = 1

    def read_token(self):
        """ Read one Token and return the Token. When the tokenizer reaches
        the end of the file, return None.
        """

        # Skip whitespaces and comments.
        self.__read_whitespace_and_comment()
        if self.__index >= self.__source_length:
            return None

        # Tokenize two character operators first. "<=" needs to be parsed as
        # TokenType.LE, not as TokenType.LT and TokenType.EQ.
        if self.__read_operator("<="):
            return Token(TokenType.LE)
        if self.__read_operator(">="):
            return Token(TokenType.GE)
        if self.__read_operator("=="):
            return Token(TokenType.EQEQ)
        if self.__read_operator("!="):
            return Token(TokenType.NOTEQ)

        # Tokenize one character operators second.
        if self.__read_operator("("):
            return Token(TokenType.LEFT_PARENTHESIS)
        if self.__read_operator(")"):
            return Token(TokenType.RIGHT_PARENTHESIS)
        if self.__read_operator("["):
            return Token(TokenType.LEFT_BRACKET)
        if self.__read_operator("]"):
            return Token(TokenType.RIGHT_BRACKET)
        if self.__read_operator("{"):
            return Token(TokenType.LEFT_BRACE)
        if self.__read_operator("}"):
            return Token(TokenType.RIGHT_BRACE)
        if self.__read_operator("*"):
            return Token(TokenType.MULTIPLY)
        if self.__read_operator("/"):
            return Token(TokenType.DIVIDE)
        if self.__read_operator("%"):
            return Token(TokenType.MOD)
        if self.__read_operator("+"):
            return Token(TokenType.PLUS)
        if self.__read_operator("-"):
            return Token(TokenType.MINUS)
        if self.__read_operator("<"):
            return Token(TokenType.LT)
        if self.__read_operator(">"):
            return Token(TokenType.GT)
        if self.__read_operator("="):
            return Token(TokenType.EQ)
        if self.__read_operator(","):
            return Token(TokenType.COMMA)
        if self.__read_operator(";"):
            return Token(TokenType.SEMICOLON)

        if (string := self.__read_string()) != None:
            return Token(TokenType.STRING, string)

        if (number := self.__read_number()) != None:
            return Token(TokenType.NUMBER, number)

        if (identifier := self.__read_identifier()) != None:
            # If the identifier is a registered keyword, return the
            # corresponding Token.
            if identifier == "and":
                return Token(TokenType.AND)
            if identifier == "or":
                return Token(TokenType.OR)
            if identifier == "if":
                return Token(TokenType.IF)
            if identifier == "else":
                return Token(TokenType.ELSE)
            if identifier == "while":
                return Token(TokenType.WHILE)
            if identifier == "break":
                return Token(TokenType.BREAK)
            if identifier == "continue":
                return Token(TokenType.CONTINUE)
            if identifier == "return":
                return Token(TokenType.RETURN)
            if identifier == "def":
                return Token(TokenType.DEF)
            if identifier == "None":
                return Token(TokenType.NONE)
            # Otherwise, return the identifier.
            return Token(TokenType.IDENTIFIER, identifier)

        DebugInfo(self).raise_exception("Undefined token found.")

    def __read_whitespace_and_comment(self):
        """ Read whitespaces (' ', '\t' and '\n') and comments. They are
        ignored by the syntax. """

        while True:
            previous_index = self.__index
            if (self.__index < self.__source_length and
                self.source[self.__index] == '#'):
                while (self.__index < self.__source_length and
                       self.source[self.__index] != '\n'):
                    self.__index += 1
            while (self.__index < self.__source_length and
                   (self.source[self.__index] == ' ' or
                    self.source[self.__index] == '\t' or
                    self.source[self.__index] == '\n')):
                if self.source[self.__index] == '\n':
                    self.line_number += 1
                    self.line_start_index = self.__index + 1
                self.__index += 1
            if previous_index == self.__index:
                return

    def __read_operator(self, operator):
        """ Read an operator specified by `operator`. Return True if the
        `operator` is found. Return False otherwise. """

        operator_length = len(operator)
        if self.__index + operator_length > self.__source_length:
            return False
        if self.source[self.__index :
                       self.__index + operator_length] == operator:
            self.__index += operator_length
            return True
        return False

    def __read_string(self):
        """ Read a string. Return the string if it's found. Return None
        otherwise. """

        assert(self.__index < self.__source_length)
        if self.source[self.__index] == '"':
            self.__index += 1
            current_index = self.__index
            while (current_index < self.__source_length and
                   self.source[current_index] != '"'):
                if self.source[current_index] == '\n':
                    self.line_number += 1
                    self.line_start_index = self.__index + 1
                current_index += 1
            if current_index >= self.__source_length:
                DebugInfo(self).raise_exception("Invalid string found.")
            string = self.source[self.__index : current_index]
            self.__index = current_index + 1
            return string
        return None

    def __read_identifier(self):
        """ Read an identifier. Return the identifier if it's found. Return
        None otherwise. """

        assert(self.__index < self.__source_length)
        current_index = self.__index
        if (self.source[current_index] == '_' or
            self.source[current_index].isalpha()):
            current_index += 1
            while (current_index < self.__source_length and
                   (self.source[current_index] == '_' or
                    self.source[current_index].isalpha() or
                    self.source[current_index].isdigit())):
                current_index += 1
            identifier = self.source[self.__index : current_index]
            self.__index = current_index
            return identifier
        return None

    def __read_number(self):
        """ Read a number. Return the number if it's found. Return None
        otherwise. """

        assert(self.__index < self.__source_length)
        if (self.source[self.__index].isdigit()):
            number = 0
            while (self.__index < self.__source_length and
                   self.source[self.__index].isdigit()):
                number = number * 10 + int(self.source[self.__index])
                self.__index += 1
            if (self.__index < self.__source_length and
                self.source[self.__index] == '.'):
                self.__index += 1
                decimal = 0.1
                while (self.__index < self.__source_length and
                       self.source[self.__index].isdigit()):
                    number += int(self.source[self.__index]) * decimal
                    decimal /= 10
                    self.__index += 1
            return number
        return None


def main(filename):
    tokenizer = Tokenizer(filename)
    while token := tokenizer.read_token():
        token.print()
        print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: %s filename" % sys.argv[0])
        exit(1)
    main(sys.argv[1])
