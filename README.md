# Programming language 'Step'

***Step*** is a mini programming language that has a Python-like syntax. The syntax is simplified as much as possible so that you can implement the interpreter in the 8 week STEP development course. The goal of the 8 week STEP development course is:

1. Implement the interpreter of Step.
1. Write a program to solve [the Travel Salesperson Problem (TSP)](https://github.com/hayatoito/google-step-tsp).
1. Run the TSP program with the interpreter.

It will be educational and inspiring to run the TSP program you wrote with the interpreter you implemented. For example, Step should be able to run [this example TSP program](./test/tsp_greedy.step).

Step is basically defined as a subset of [Python3](https://docs.python.org/3/) with one exception that Step does not use Python3's indent rule. Step uses `;` to define a statement and `{` and `}` to define a statement block because this simplifies the interpreter implementation.

Example:
```
a = 123.0;            # Number
b = "abc";            # String
c = None;             # None
d = [1, 2, 3];        # List
e = [[1, 2], [3, 4]]; # Two-dimensional list

if (a > 100) {        # If statement
    print("Foo");     # Call a builtin function
} else {
    print("Bar");
}

i = 0;
while (i < 10) {      # While statement
    if (i < 5) {
        continue;     # continue
    }
    if (i == 8) {
        break;        # break
    }
    i = i + 1;
}

def function(a, b) {  # Define a function
    return a + b;     # return
}

function(100, 200);   # Call the function
```

# Syntax

This section informally defines **at least what syntax must be supported**. It does not define a full syntax of Step. Syntax about edge cases and advanced cases are intentionally omitted to minimize the complexities so that you can finish implementing the core part of the interpreter within the 8 week STEP development course. **For syntax that is not defined here, you can extend as you like. Be creative!**

## Data types

Step supports five data types: numbers, strings, lists, functions and None.
```
123;                  # number
123.01;               # number
"abc";                # string
[1, 2, 3];            # list
def function(x, y) {  # function
    return x + y;
}
None;                 # None
```

A number may be an integer or a floating point number. Similarly to Python3, the conversion is done automatically.
```
a = 123;      # Integer (123)
a = a + 1;    # Integer (124)
a = a + 1.0;  # Floating point number (125.0)
```

A string may contain only ASCII characters.

A list may be multi-dimensional.
```
a = [[1, 2], [3, 4]];  # Two-dimensional list.
print(a[1][1]);        # 4
```

A function may be assigned to a variable and called.
```
def function(x, y) {    # function
    return x + y;
}
print(function(2, 3));  # 5
a = function;
print(a(4, 5));         # 9
```

Note: You may skip implementing functions in the initial version. The test programs including TSP are written without using functions.

## True / False

Step does not have boolean types (True / False). The following values are evaluated as false. Other values are evaluated as true.

* 0
* An empty string `""`.
* An empty list `[]`.
* None.

```
if (0) {
    ... # This code does not run.
}
if ("") {
    ... # This code does not run.
}
if ([]) {
    ... # This code does not run.
}
if (None) {
    ... # This code does not run.
}
if (1) {
    ... # This code runs.
}
```

## Variables

For simplicity, Step has only global variables. There are no local variables.

Note: This is inconvenient. You may support local variables if you want.

```
def function(a) {
    b = 200;
}

a = 1;
b = 2;
print(a);        # 1
print(b);        # 2
function(100);
print(a);        # 100
print(b);        # 200
```

## Comments

A comment starts with '#' that is not part of a string, and ends at the end of the line ('\n').
```
a = 100;  # This is a comment.
a = "abc # this is part of a string and not a comment";
```

## Operators

Some operators do not support all data types. For example, `4 / 3` is supported but `"abcd" / "abc"` is not supported. The following describes **at least what operations must be supported**. For unsupported operations, you can throw an exception and stop the program execution. You may extend the support as you like.

### +
```
# <number> + <number>
print(2 + 3.0);  # 5.0

# <string> + <string>
print("abc" + "def");  # "abcdef"

# <list> + <list>
print([1, 2] + [3, 4]);  # [1, 2, 3, 4]
```

### -
```
# <number> - <number>
print(2 - 3.0);  # -1.0

# - <number>
print(-100);     # -100
```

### *
```
# <number> * <number>
print(2 * 3.0);  # 6.0

# <string> * <number>
print("abc" * 3);  # "abcabcabc"

# <number> * <string>
print(3 * "abc");  # "abcabcabc"

# <list> * <number>
print([1, 2] * 3);  # [1, 2, 1, 2, 1, 2]

# <number> * <list>
print(3 * [1, 2]);  # [1, 2, 1, 2, 1, 2]
```

### /
```
# <number> / <number>
print(6 / 4);  # 1.5
```

The semantics follows Python3's `/`. `6 / 4` is evaluated as `1.5`, not `1`.

### %
```
# <number> % <number>
print(6 % 4);   # 2
```

The semantics follows Python3's `%`.

### ()
`()` changes the priority of the expression.
```
(3 + 4) * 5;  # 35
```

### []
```
# <string> [ <number> ]
x = "abc";
print(x[0]);  # "a"
print(x[2]);  # "c"

# <list> [ <number> ]
x = [1, 2, [3, 4]];
print(x[0]);     # 1
print(x[2]);     # [3, 4]
print(x[2][0]);  # 3
```

### =
```
# <identifier> = <any data>
a = 100;
b = a;
print(b);       # 100

# <list> [ <number> ] = <any data>
a = [1, 2, [3, 4]];
a[0] = 100;
a[2][0] = 300;
print(a);       # [100, 2, [300, 4]]
```

### <, >, <=, >=
```
# <number> < <number>
print(1 < 2);   # 1

# <number> <= <number>
print(1 <= 2);  # 1

# <number> > <number>
print(1 > 2);   # 0

# <number> >= <number>
print(1 >= 2);  # 0
```

Step does not have boolean values (True / False). `<`, `>`, `<=` and `>=` returns 1 or 0.

### ==, !=
`==` and `!=` support all data types. `==` returns 1 for the following cases and 0 otherwise.

* The left side is a number, the right side is a number, and the two numbers are equal.
* The left side is a string, the right side is a string, and the two strings are equal.
* The left side is a list, the right side is a list, and all the items in the two lists are equal.
* The left side is a function, the right side is a function, and the two functions are equal.
* The left side is None, and the right side is None.

`!=` returns 1 when `==` returns 0. `!=` returns 0 when `==` returns 1.

```
print(1 == 1);            # 1
print("abc" == "abc");    # 1
print([1, 2] == [1, 2]);  # 1
print([1, [2, "abc"]] == [1, [2, "abcd"]]);  # 0
print(print == print);    # 1
print(None == None);      # 1
print(1 == None);         # 0
print("print" == print);  # 0
```

### and, or
`and` returns 1 when both the left side and the right side are evaluated as true, and returns 0 otherwise.
```
print(1 and 1);  # 1
print(1 and 0);  # 0
print(0 and 1);  # 0
print(0 and 0);  # 0
```

`or` returns 1 when the left side or the right side are evaluated as true, and returns 0 otherwise.
```
print(1 or 1);  # 1
print(1 or 0);  # 1
print(0 or 1);  # 1
print(0 or 0);  # 0
```

## Statements

### if
```
if (condition) {
    ...;
} else {
    ...;
}
```

For simplicity, Step does not support `elif` (but you may support it).

### while
```
while (condition) {
    ...;
}
```

For simplicity, Step does not support `for` (but you may support it).

### break, continue
```
i = 0;
while (i < 10) {
    if (i < 5) {
        continue;     # continue
    }
    if (i == 8) {
        break;        # break
    }
    print(i);         # This prints 5, 6 and 7.
    i = i + 1;
}
```

### function, return
```
def function(a, b) {
    if (a > b) {
        return "abc";
    }
    if (a == b) {
        return [1, 2];
    }
    return;
}

print(function(2, 1));  # "abc"
print(function(2, 2));  # [1, 2]
print(function(2, 3));  # None
a = function;
print(a(2, 1));  # "abc"
print(a(2, 2));  # [1, 2]
print(a(2, 3));  # None
```

Note: You may skip implementing functions in the initial version. The test programs including TSP are written without using functions.

## Builtin functions

Step supports at least the following builtin functions, which are needed to write basic programs including TSP. You may add more builtin functions as needed.
```
# print(): print values, followed by a line break.
print(1, "abc", [1, 2]);

# assert(condition, message): If the `condition` is false, print the `message`
# and stop the program execution. The `message` is optional.
x = 1;
assert(x == 1);  # Do nothing
assert(x == 1, "x should be 1");  # Do nothing.
assert(x == 2, "x should be 1");  # Print the message and stop the program execution.
assert(x == 2);  # Print nothing and stop the program execution.

# len(value): Python3's len(). If the `value` is a string or a list, returns
# the length.
print(len("abc"));      # 3
print(len([1, 2, 3]));  # 3

# int(value): Python3's int(). Convert the `value` to an integer.
print(int("123"));  # 123

# str(value): Python3's str(). Convert the `value` to a string.
print(str(123));        # "123"
print(str([1, 2, 3]));  # "[1, 2, 3]"
print(str(None));       # None

# sqrt(value): Python3's math.sqrt(). If the `value` is a number, return the
# square root of the value.
print(sqrt(144.0));  # 12.0

# append(list, value): Python3's list.append(value). If the `list` is a list,
# append the `value` to the list.
a = [];
append(a, 1);
append(a, "abc");
print(a);          # [1, "abc"]
```

## Formal syntax definition

For the formal syntax definition, please see [tokens.txt](./tokens.txt) and [bnf.txt](./bnf.txt).

# Tests

You can use the following tests to test the interpreter you implemented.

* `test/basic_unittests.step`: All unittests except functions.
* `test/advanced_unittests.step`: Unittests for functions. If you skip implementing functions, you don't need to run this test.
* `test/prime.step`: Test to calculate the 100-th prime number. This does not use functions.
* `test/matrix.step`: Test to calculate a matrix multiplication. This does not use functions.
* `test/tsp_greedy.step`: Test to solve TSP with a greedy algorithm. This does not use functions.

