llc -filetype=obj meu_modulo.ll -o root.o
clang -shared -fPIC io.c -o io.so
clang -S -emit-llvm -o io.bc -c io.c
llc -filetype=obj io.bc -o io.o
clang root.o io.o -o root.exe
