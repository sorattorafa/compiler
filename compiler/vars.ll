; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"a" = common global i32 0, align 4
define i32 @"func"() 
{
entry:
  %"c" = alloca i32, align 4
  store i32 10, i32* @"a"
  store i32 2, i32* %"c"
}

define i32 @"principal"() 
{
entry:
  %"b" = alloca i32, align 4
  store i32 a, i32* %"b"
  store i32 10, i32* @"a"
}
