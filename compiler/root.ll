; ModuleID = "geracao-codigo-tpp.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

@"p" = common global i32 0, align 4
@"t" = common global i32 0, align 4
define i32 @"func"(i32 %"p", i32 %"t") 
{
entry:
  %"r" = alloca i32, align 4
  store i32 1, i32* %"r"
  br label %"exit"
exit:
  %"ret_temp" = load i32, i32* %"r", align 4
  ret i32 %"ret_temp"
}

define i32 @"main"() 
{
entry:
  %"x" = alloca i32, align 4
  store i32 1, i32* @"t"
  store i32 2, i32* @"p"
  %"x.1" = alloca i32
  %".4" = load i32, i32* @"t"
  %".5" = load i32, i32* @"p"
  %".6" = call i32 @"func"(i32 %".4", i32 %".5")
  store i32 %".6", i32* %"x.1"
  br label %"exit"
exit:
  ret i32 0
}
