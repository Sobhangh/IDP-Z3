function! Folint_callback(bufnr, lines) abort
    let result = []

    for line in a:lines
        let matches = matchlist(line, '\(Error\|Warning\): line \(\d\+\) - colStart \(\d\+\) - colEnd \(\d\+\) => \(.*\)')

        if len(matches) >= 2
            if matches[1] == 'Error'
                let type = 'E'
            else
                let type = 'W'
            endif

            let element = {
                        \ 'text': matches[5],
                        \ 'detail': 'none',
                        \ 'lnum': matches[2],
                        \ 'col': matches[3],
                        \ 'end_col': matches[4],
                        \ 'type': type
                        \ }
            call add(result, element)
        endif
    endfor

    return result
endfun

" https://dhilst.github.io/2021/03/27/Adding-linters-to-ALE.html
call ale#linter#Define('idp', {
\ 'name': 'folint',
\ 'lint_file': 1,
\ 'executable': 'FOlint',
\ 'command': '%e %t',
\ 'project_root': './',
\ 'callback': 'Folint_callback'
\    })
