from scanner import *
from parser import *

#input_string = '''
#x := 5;
#y := x;
#PRINT 64;
#'''

input_string = '''
  version: "3.9"
'''

print input_string
scanner = Scanner(input_string)
print(scanner.tokens)

parser = Parser(scanner)
parser.start()
  
