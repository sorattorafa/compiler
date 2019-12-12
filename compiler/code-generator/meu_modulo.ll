; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"A" = common global [1024 x i64] undef, align 16
define i64 @"main"() 
{
entry:
  %"retorno" = alloca i64
  store i64 0, i64* %"retorno"
  %"B" = alloca [1024 x i64], align 16
  %"ptr_A_49" = getelementptr [1024 x i64], [1024 x i64]* @"A", i64 0, i64 49
  %".3" = load i64, i64* %"ptr_A_49", align 4
  br label %"exit"
exit:
  %".5" = load i64, i64* %"retorno"
  ret i64 %".5"
}
