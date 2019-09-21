if !has("python3")
    finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
sys.path.append(plugin_root_dir)

from fugitive_pagure import main
EOF

function! s:function(name) abort
    return function(substitute(a:name,'^s:',matchstr(expand('<sfile>'), '<SNR>\d\+_'),''))
endfunction


function! s:pagure_url(opts, ...)
    python3 main()
    return s:url
endfunction


if !exists('g:fugitive_browse_handlers')
    let g:fugitive_browse_handlers = []
endif

call insert(g:fugitive_browse_handlers, s:function("s:pagure_url"))
