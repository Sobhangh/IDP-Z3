" ftplugin/idp.vim
" Author: Simon Vandevelde <simonvandevelde.be>
setlocal commentstring=//\ %s
setlocal iskeyword+=?,!,#  " This also influences what is considered as part of a sentence.
setlocal tabstop=4
setlocal softtabstop=4
setlocal shiftwidth=4
setlocal completefunc=syntaxcomplete#Complete
