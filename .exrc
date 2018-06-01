if &cp | set nocp | endif
let s:cpo_save=&cpo
set cpo&vim
imap <C-BS> 
nmap  o
map  :bn 
map  :bp 
map  :bd 
map ,g :source ~/.gvimrc 
map ,v :source ~/.vimrc 
noremap H gT
nnoremap L gt
nnoremap Wa wa
vmap gx <Plug>NetrwBrowseXVis
nmap gx <Plug>NetrwBrowseX
vnoremap <silent> <Plug>NetrwBrowseXVis :call netrw#BrowseXVis()
nnoremap <silent> <Plug>NetrwBrowseX :call netrw#BrowseX(expand((exists("g:netrw_gx")? g:netrw_gx : '<cfile>')),netrw#CheckIfRemote())
nmap <S-CR> O
iabbr slef self
iabbr defien define
iabbr raneg range
iabbr seperate separate
iabbr teh the
let &cpo=s:cpo_save
unlet s:cpo_save
set background=dark
set backspace=indent,eol,start
set fileencodings=ucs-bom,utf-8,default,latin1
set helplang=en
set hidden
set hlsearch
set ignorecase
set incsearch
set nomodeline
set printoptions=paper:letter
set ruler
set runtimepath=~/.vim,/var/lib/vim/addons,/usr/share/vim/vimfiles,/usr/share/vim/vim74,/usr/share/vim/vimfiles/after,/var/lib/vim/addons/after,~/.vim/after
set showcmd
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc
set textwidth=80
set wildignore=*.o,*.obj,*.bak,*.exe
" vim: set ft=vim :
