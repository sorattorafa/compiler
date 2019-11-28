; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = common global i32 0, align 4
define i32 @"principal"() 
{
entry:
  %"ret" = alloca i32, align 4
  store i32 10, i32* @"a"
  %"a_cmp" = load i32, i32* @"a", align 4
  %"if_test_1" = icmp sgt i32 %"a_cmp", 5
  br i1 %"if_test_1", label %"iftrue_1", label %"iffalse_1"
iftrue_1:
  store i32 1, i32* %"ret"
  br label %"ifend_1"
iffalse_1:
ifend_1:
exit:
  %"ret_temp" = load i32, i32* %"ret", align 4
  ret i32 %"ret_temp"
}
