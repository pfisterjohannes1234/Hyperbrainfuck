# Hyperbrainfuck

## TL;DR

A Brainfuck variant with an extra B command.

It has infinite cells and there is no cell value limit.
EOF is -1.
Output values are clamped at 0 and 255.

The B command calculates the Busy beaver value of the current cell value and replaces the cell value
 with it.


The name Hyper for Hypercomputation and brainfuck since everything else is Brainfuck.

## Goal

The Goal is to have a programming language that is capable of doing hypercomputation.
That means, it can calculate things that can not be calculated with a turing machine.
The impossibility to do that with a turing machine isn't about functions that interact with external
 features (open files, control a serial port, connect to a server, ... ) nor about getting random
 data but a pure computability.

The rest of the language should be very simple to define. For that, we use a Brainfuck variant.

## Hypercomputation

To have a language that is hypercomputationable, we define a programming language that has an oracle
 that can solve some halting problems.
In this case, we choose to use the Busy Beaver function and define that a fully compilant
 environment (interpreter, OS, hardware, ...) needs to have an oracle that tells the Busy Beaver
  numbers.
Using the Busy Beaver function has the nice sideeffect, that we can create a non-compilant
 environment that has the exact same behaviour as a fully compilant environment in the real world,
 since the difference would only be detectable after an extremely large amount of executed
 instructions so that, assuming a non-optimizing environment is used, no human could ever observere
 it.

## Language Definition

### Schematic

```
Program code as Command string:

Program Code: ,+[-.>,+]
                    ^
                    | Instruction pointer


Infinite Tape of data Cells:

                         | Cell pointer
                         V
Infinite    -+----+----+----+----+-     Infinite
cells to ... | 55 | 12 | -1 |  0 | ...  cells to
the left    -+----+----+----+----+-     the right

```

### Description

A program is a arbitary long string of command characters.
The string has a set order of characters.
A instruction pointer points a command character.
Initinally, the instruction pointer points to the first character of the command string.
The command pointed by the command pointer is executed, after that the command pointer moves to the
 next command character.

The program operates on a infinite tape of cells, infinite in both directions.
Every cell holds a integer value, there is no limit of what value a single cell can hold.
A cell pointer points to a cell on this tape.
The pointer can be moved to the right and to the left.
The cell pointer by the cell pointer is the current cell

### Commands

| Command  | Name      | Definition                                                                        |
|----------|-----------|-----------------------------------------------------------------------------------|
| +        |Increment  | Increment the cell value of the current cell                                      |
| -        |Decrement  | Decrement the cell value of the current cell                                      |
| >        |Go right   | Move the cell pointer to the next cell to the right                               |
| <        |Go left    | Move the cell pointer to the previous cell to the left                            |
| [        |Start Loop | If the current cell is 0, jump forward to the matching ], otherwise do nothing    |
| ]        |End Loop   | If the current cell is 0, do nothing. Otherwise jump to the previously matching [ |
| ,        |Read       | Read a single occet from the input stream and replace the current cell value with it  |
| .        |Write      | Writes the current cell value to the output stream, clamped to 0 and 255          |
| B        |Busy beaver| Calculate the Busy beaver Σ() value of the current cell and replace that cell value with the result  |


#### Increment and decrement

This increments or decrements the value of the current cell by 1.
Since there is no limit a value can have, it doesn't wrap around or stops anywhere, it will
 increment or decrement without limits.

####  Go right or left

This moves the cell pointer to the cell to the left or to the right, and therefore changes the
 current cell.
All cell values are unchanged.
Since there is an infinite amount of cells to the left and to the right, there are no special cases
 to be considered.

####  Loops

Loops start with a `[` and and with a matching `]`.
Matching means there are the same number of `[` and `]` in between 2 matching `[]`.
From the beginning of the command string till any point in the command string, there are never more
 `]` commandds then there are `[` commandds. Similar, from any point in the command string to
 the end, there are never more `[` commandds than there are `]` characters.

A loop is repeatet as long as the current cell is not 0.
That means, if the instruction pointer reaches a `[`, the current cell is checked and if it is 0,
 the instruction pointer jumps to the matching `]` and continues with the first command after this
 `]`. If the cell is not 0, the instruction pointer is not changed and will continue after the `[`.
And when the instruction pointers reaches a `]`, the current cell is checked and if it is 0, the
 instruction pointer is not changed and will continue after the `]`. If the cell is not 0, the
 instruction pointer jumps to the matching `[` and will continue after this `[`.



####  Read and Write

The environment provides a input and a output stream of numbers.

A read command reads the next number, a value from 0 to 255, from the input stream and replaces the
 current cell value with the readed value.
If there is no input left, the cell value is changed to -1.

A write command outputs the current cell value to the output stream.
If the current cell value is less than 0, 0 is outputed, if the value is more than 255, 255 is
 outputed.


### Busy beaver Command `B`

For Hyperbrainfucks `B` command, we use the Busy beaver function $Σ()$ of a 2 symbol and `n` state
 machine.
`n` is the cell value before the `B` command is executed.
If `n` is less than 1, the result is considered 0 (for this language definition).

The Busy beaver function $Σ(n,2)$ returns the maximum number of `1`'s any turing machine with `n`
 states and 2 symbols can write to its initially all `0` tape and still halt.
The first 5 Busy beaver values $Σ(n,2)$ are:


| n | Σ(n,2) |
| - |--------|
| 0 | 0 / NA |
| 1 |      1 |
| 2 |      4 |
| 3 |      6 |
| 4 |     13 |
| 5 |   4098 |

After that, the results grows extremly fast, with $n=6$ the result is already $>10↑↑15$.

The definition of a turing machine is not part of this document.

## Similar Projects

The Brainfuck extension One from Tailcalled ( https://esolangs.org/wiki/One_(Tailcalled) ).
It also extens Brainfuck with Hypercomputation instruction, but not with the Busy Beaver of a
 Turing machine and i don't know any values of One's I instruction.






