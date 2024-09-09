#!/usr/bin/python
#
# A interpreter for the Hyperbrainfuck language.
# The interpretation is limited.
# It doesn't have infinite amount of cells nor does it support infinite cell values
# The Busy Beaver command B is only calculated to values up to 5, after that, we consider the value
# as infinite, since it is so large we can not calculate it nor store it.
#
# Public Domain licence

helptext=\
"""
Hyperbrainfuck interpreter.

Hyperbrainfuck commands:
+ Increment current cell
- Decrement current cell
> Move to next cell
< Move to previous cell (here: stay at cell 0 if we are already at cell 0)
[ if cell value is 0, move to next command after the corresponding ]. If value is not 0, continue with command after [
] jump to corresponding [
, read value
. output value clamped to 0 to 255
B Calculate the Busy beaver function Σ(n,2) with the current cell value and replace the cell with result.

Give the Hyperbrainfuck code as first argument
"""

import sys


def error(message):
  print(message,file=sys.stderr)
  exit(1)

def codeCheckShorten(code):
  deep = 0
  l =[]
  for i in code:
    if i not in ['[',']','+','-','<','>',',','.','B']:
      continue
    if i==']':
      deep=deep-1
      if deep<0:
        error("To many ] before enough [")
    if i=='[':
      deep=deep+1
    l.append( i )
  if deep != 0:
    error("[ and ] does not match")
  return l

  
def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def execute(code):
  bracemap = buildbracemap(code)
  codeptr  = 0

  tape = [0]
  tapeIndex = 0

  while codeptr < len(code):
    command = code[codeptr]
    v = tape[tapeIndex]

    if command == ">":  
      tapeIndex=tapeIndex+1
      if tapeIndex>=len(tape):
        tape=tape+[0]
    if command == "<":  
      tapeIndex=tapeIndex-1
      if tapeIndex<0:
        tapeIndex=0
        tape=[0]+tape
    if command == "+":  tape[tapeIndex] = v+1
    if command == "-":  tape[tapeIndex] = v-1

    if command == "[" and v == 0: codeptr = bracemap[codeptr]
    if command == "]" and v != 0: codeptr = bracemap[codeptr]

    if command == ".":
      v = 255 if v>255 else 0 if v<0 else v
      print( v )
    if command == ",":
      def getValue():
        while 1:
          c= sys.stdin.readline()
          if len(c) == 0: #EOF
            return -1
          v = int(c)
          if v>255:
            print("Input value too large, must be less than 256")
            continue
          if v<0:
            print("Input value can not be negativ")
            continue
          return v
      v = getValue()
      tape[tapeIndex]=v
      if len(s):
        return int(s)
      return None
    if command == "B":
      if   v<=0:   tape[tapeIndex]=0
      elif v==1:   tape[tapeIndex]=1
      elif v==2:   tape[tapeIndex]=4
      elif v==3:   tape[tapeIndex]=6
      elif v==4:   tape[tapeIndex]=13
      elif v==5:   tape[tapeIndex]=4098
      elif v>=6:   tape[tapeIndex]=float("inf")
      
    codeptr = 1+codeptr



def main():
  if len(sys.argv)!=2:
    error("Ussage: "+sys.argv[0]+" <program code>")
  code = sys.argv[1]
  code = codeCheckShorten( code )
  execute( code )



if __name__ == "__main__": main()


