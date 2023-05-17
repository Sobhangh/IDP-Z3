# FOLint support in Vim/Neovim and more

This is a brief guide detailing how to set up the FOLint tool in Vim/Neovim, and how to enable syntax highlighting/automatic indentation for IDP.

## FOLint with ALE

FOLint is a linting tool for FO(·), a language used by the IDP system.

A popular Vim plugin to support linting is [ALE](https://github.com/dense-analysis/ale), which already comes with support for many linters.
We can extend it with support for FOLint by adding a custom linter.

Firstly, we need to modify our `.vimrc` so that it recognizes the `.idp` file extension and we need to tell ALE that we can use FOLint.
```vim
au BufNewFile,BufRead *.idp set filetype=idp
let g:ale_linters = {
    \   'idp': ['folint']
    \}
```

Then we configure the linter itself in ALE.
ALE collects all its linters in `~/.vim/bundle/ale/ale_linters/<language>`.
After creating an `idp` folder in that location, save the following vimscript as `folint.vim`:

```vim
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
\ 'executable': 'folint',
\ 'command': '%e %t',
\ 'project_root': './',
\ 'callback': 'Folint_callback'
\    })
```

## FOLint with null-ls (Neovim)

[null-ls](https://github.com/jose-elias-alvarez/null-ls.nvim) is a popular Neovim plugin for non-LSP sources to hook into Neovim's LSP client.
This allows linters to hook into Neovim's LSP diagnostics.

This requires Neovim to recognize the IDP filetype as specified above. Below you can find a lua version for this.
```lua
vim.api.nvim_create_autocmd(
  { "BufNewFile", "BufRead" },
  {
    pattern = { "*.idp" },
    command = [[set filetype=idp]],
  }
)
```

Next we need a null-ls source for FOLint and register it:
```lua
local null_ls = require'null-ls'
local helpers = require'null-ls.helpers'

local folint = {
  name = "FOLint",
  method = null_ls.methods.DIAGNOSTICS_ON_SAVE,
  filetypes = { "idp" },
  generator = helpers.generator_factory{
    args = { "$FILENAME" },
    command = "folint",
    format = "line",
    on_output = helpers.diagnostics.from_pattern(
      [[((%u)%w+): line (%d+) -- colStart (%d+) -- colEnd (%d+) => (.*)]],
      {"code", "severity", "row", "col", "col_end", "message"}
    )
  },
}

-- then add it to your null-ls setup
null_ls.setup{
  sources = {
    -- other sources
    folint,
    -- more sources
  }
}

-- or register it separately
null_ls.register(folint)

```

## Syntax highlighting

This repo also contains configuration files to set up syntax highlighting for FO(·) in Vim (based on [this guide](https://thoughtbot.com/blog/writing-vim-syntax-plugins) by thoughtbot).
Installing them yourself is quite a simple task.
This assumes you already set up your vimrc to include the IDP filetype info.

There are three files:

* `ftplugin/idp.vim`, a script run when opening IDP files. It tells Vim what the special symbols are, wath the width of a tab symbol is, ...
* `syntax/idp.vim`, which configures syntax highlighting.
* `indent/idp.vim`, which configures automatic indentation.

To install these, move them to your `~/.vim` folder.
Make sure to include the folders, so `~/.vim/ftplugin/idp.vim`, `~/.vim/syntax/idp.vim` and `~/indent/idp.vim`.
