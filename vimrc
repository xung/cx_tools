"开启语法高亮
set nocompatible "不要vim模仿vi模式，建议设置，否则会有很多不兼容的问题
syntax on
"自动检测文件类型并加载相应的设置
filetype plugin indent on
"tab替换为4个空格
autocmd FileType python setlocal et sta sw=4 sts=4
autocmd FileType awk,c,cpp,sh set shiftwidth=4
"显示行号
set number
"为方便复制，用<F2>开启/关闭行号显示:
nnoremap <F2> :set nonumber!<CR>:set foldcolumn=0<CR>
set nocompatible "不要vim模仿vi模式，建议设置，否则会有很多不兼容的问题
set nowrap "不自动换行
set hlsearch "高亮显示结果
set incsearch "在输入要搜索的文字时，vim会实时匹配
set backspace=indent,eol,start whichwrap+=<,>,[,] "允许退格键的使用
"字体的设置
set guifont=Bitstream_Vera_Sans_Mono:h9:cANSI "记住空格用下划线代替哦
let &termencoding=&encoding
set fileencodings=utf-8,gbk,ucs-bom,cp936
set cursorline
"显示tab及显示替换
set list
set listchars=tab:>-

"py文件执行
autocmd FileType python map <F8> <Esc>:w!<CR>:!python %<CR>
"python补全
"1. pythoncomplete补全
autocmd FileType python set omnifunc=pythoncomplete#Complete
"2. Pydiction插件补全
let g:pydiction_location = '~/.vim/myplugin/pydiction/complete-dict'


set tags=tags;/
let Tlist_Show_One_File=1
let Tlist_Exit_OnlyWindow=1
"let g:winManagerWindowLayout='FileExplorer|TagList'
let g:winManagerWindowLayout='TagList'
nmap wm :WMToggle<cr> 
