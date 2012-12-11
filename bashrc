export http_proxy="http://xung:search@10.12.167.31:808"
export https_proxy="http://xung:search@10.12.167.31:808"
PS1='[\[\e[32m\]\u@\[\e[36m\]\h \w]\$\[\e[m\] '

# alias set
#grep history
alias hg="history | grep"
#cmake debug mode
alias cmaked="cmake -DCMAKE_BUILD_TYPE:STRING=Debug"
#cmake release mode
alias cmaker="cmake -DCMAKE_BUILD_TYPE:STRING=Release"
alias gsrc='grep -rn --include="*.cpp" --include="*.h"'
