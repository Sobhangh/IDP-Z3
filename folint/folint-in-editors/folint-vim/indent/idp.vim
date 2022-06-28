" indent/idp.vim
" Automatically decide indent level when creating new line.
" Author: Simon Vandevelde <simonvandevelde.be>

setlocal indentexpr=IdpIndent()

function! IdpIndent()
    let line = getline(v:lnum)
    let previousNum = prevnonblank(v:lnum - 1)
    let previous = getline(previousNum)

    " =~ is the regex match operator.
    " Increase indent when opening new block.
    if previous =~ "vocabulary" || previous =~ "theory" || previous =~ "Structure" || previous =~ "procedure"
        return indent(previousNum) + &tabstop
    endif

    if !(previous =~ ".")
        return indent(previousNum) + &tabstop
    endif

    if previous =~ "{"
        return indent(previousNum) + &tabstop
    endif

    if previous =~ "}"
        return indent(previousNum) - &tabstop
    endif

    return indent(previousNum)

endfunction
