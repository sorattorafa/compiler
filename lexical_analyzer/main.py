from lexer import MyLexer 
import ply.lex as lex 
from sys import argv  
 
m = MyLexer()
m.build()           # Build the lexer  
f = open(argv[1])  
# input data
m.test(f.read())     # Test it  
#print(len(argv))