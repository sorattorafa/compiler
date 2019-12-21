; ModuleID = "geracao-codigo-tpp.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

define i32 @"main"() 
{
entry:
  %"x" = alloca i32, align 4
  %"y" = alloca float, align 4
  store i32 0, i32* %"x"
  store float              0x0, float* %"y"
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"x"
  %".6" = call float @"leiaFlutuante"()
  store float %".6", float* %"y"
  %".8" = load i32, i32* %"x"
  call void @"escrevaInteiro"(i32 %".8")
  %".10" = load float, float* %"y"
  call void @"escrevaFlutuante"(float %".10")
  br label %"exit"
exit:
  ret i32 0
}
