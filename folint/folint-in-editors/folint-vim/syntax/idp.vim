" syntax/idp.vim
" This file dictates the syntax highlighting for IDP's FO(.) code.
" Author: Simon Vandevelde <simonvandevelde.be>
syntax keyword idpBlock vocabulary theory structure procedure Vocabulary Theory Structure Procedure
syntax keyword idpTodo TODO FIXME XXX Todo todo
syntax keyword idpBuiltinType Bool Real Int 𝔹 ℤ ℝ

" Match all idp keywords
syntax keyword idpKeyword type
syntax match idpKeyword "[:|#|{|}|(|)|,|*]"
syntax match idpKeyword ":="
syntax match idpKeyword "->"

syntax region idpComment start=/\/\// end=/$/ oneline

highlight default link idpBlock Identifier
highlight default link idpTodo Todo
highlight default link idpBuiltinType Type
highlight default link idpKeyword Label

highlight default link idpComment Comment
