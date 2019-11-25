; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"() 
{
entry:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  store i32 1, i32* %"a"
  store i32 2, i32* %"b"
  store i32 0, i32* %"c"
  %"a_cmp" = load i32, i32* %"a", align 4
  %"b_cmp" = load i32, i32* %"a", align 4
  %"if_test_1" = icmp slt i32 %"a_cmp", %"b_cmp"
  br i1 %"if_test_1", label %"iftrue_1", label %"iffalse_1"
exit:
  %".17" = load i32, i32* %"retorno"
  ret i32 %".17"
iftrue_1:
  store i32 5, i32* %"c"
  br label %"ifend_1"
iffalse_1:
  store i32 6, i32* %"c"
  br label %"ifend_1"
ifend_1:
  %"a_cmp_2" = load i32, i32* %"a", align 4
  %"if_test_1.1" = icmp slt i32 %"a_cmp", 1024
  br i1 %"if_test_1.1", label %"iftrue_2", label %"iffalse_2"
iftrue_2:
  store i32 10, i32* %"c"
  br label %"ifend_2"
iffalse_2:
  store i32 20, i32* %"c"
  br label %"ifend_2"
ifend_2:
  br label %"exit"
}
