; ModuleID = "geracao-codigo-tpp.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

define i32 @"soma"(i32 %"a", i32 %"b") 
{
entry:
  %"a.1" = alloca i32
  %"b.1" = alloca i32
  %".4" = load i32, i32* %"a.1"
  %".5" = load i32, i32* %"b.1"
  %"add" = add i32 %".4", %".5"
  br label %"exit"
exit:
  %".7" = add i32 %"a", %"b"
  ret i32 %".7"
}

define i32 @"main"() 
{
entry:
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"c.1" = alloca i32
  %".2" = load i32, i32* %"a"
  %".3" = load i32, i32* %"b"
  %".4" = call i32 @"soma"(i32 %".2", i32 %".3")
  store i32 %".4", i32* %"c.1"
  br label %"exit"
exit:
  %"ret_temp" = load i32, i32* %"c", align 4
  ret i32 %"ret_temp"
}

declare i32 @"leiaInteiro (a)"(i8* %".1", ...) 

declare i32 @"leiaInteiro (b)"(i8* %".1", ...) 

declare void @"escreva_valor (c)"() 
