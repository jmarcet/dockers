
# Activate 'pyrocore' virtualenv
#test ! -f ~/.local/pyroscope/bin/activate || . ~/.local/pyroscope/bin/activate

# rTorrent aliases
alias rtlistmethods="( rtxmlrpc system.listMethods ; rtxmlrpc system.has.private_methods | sed -re 's/$/ \[prv]/' ) | sort | egrep"
alias rtjustnow="rtcontrol loaded=-5i -qofiles"
alias rt2days="rt-completion completed=-2d"
alias rt7days="rt-completion completed=-7d"
alias rt-completion="rtcontrol --column-headers -scompleted -ocompletion"
alias rtls="rtcontrol -qo '{{chr(10).join([d.directory+chr(47)+x.path for x in d.files])|h.subst(chr(47)+chr(43),chr(47))}}'"
alias rt-stats-msg="rtcontrol -q -s alias,is_open,message -o alias,is_open,message 'message=?*' message=\!*Tried?all?trackers* | uniq -c"
alias rt-stats-seeding='rtcontrol --summary -qco leechtime,seedtime,size.sz,uploaded.sz,ratio.pc'
alias rt-stats-trackers='rtcontrol -s alias -qo alias '\''*'\'' | uniq -c | sort -n'

# Shortcuts to internal commands
alias rt-ui-categories="python-pyrocore -m pyrocore.ui.categories"
alias rt-ui-themes="python-pyrocore -m pyrocore.ui.theming"
