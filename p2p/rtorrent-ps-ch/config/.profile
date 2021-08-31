# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# include common alises like functions and export them
. ~/.profile_rtfunctions && export RTHOME && export -f rtlistOrphans rtlistOrphanMetas rtlistPublic rtlistStuck rtlistMessages rtlistStopped rtgetTotalRotatingSize

# include pyrocore tools alias definitions
if [ -f ~/.pyroscope/rt_aliases.sh ]; then
    . ~/.pyroscope/rt_aliases.sh
fi

# Automatically reattach the rtorrent session or create a new one only if STDIN is a terminal (we are using interactive mode)
# if [ -t 0 ] && [ -z "$TMUX" ]; then 
#     tmux -2u new-session -A -s rtorrent 
# fi
