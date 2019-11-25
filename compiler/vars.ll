; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = common global i32 0, align 4
define i32 @"main"() 
{
entry:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"a" = alloca i32, align 4
  store i32 10, i32* %"a"
  %"b" = alloca i32, align 4
  store i32 a, i32* %"b"
  br label %"exit"
exit:
  %".6" = load i32, i32* %"retorno", align 4
  ret i32 %".6"
}
