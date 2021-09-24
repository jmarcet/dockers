#!/bin/bash
# Send email report about any stuck torrent in incomplete directory
# Usage: reportStuck.sh


# include the helper script
. "${BASH_SOURCE%/*}/rtUtils.sh"

# subject of email report
REPORTSUBJECT="List of Stuck torrents in 'incomplete' dir"

# text for email at the beginning
REPORTBODY="There are stuck torrents in 'incomplete' directory, manual interaction is required."


# checking for rtorrent problems and the existence of rtcontrol util
if [ ! "$MAILHELPERRTSTATUSVAL" = true ] && [ -L "$RTCONTROLBIN" ]; then
    # prepare report and set optional subject and text for potentional email
    prepareReport rtlistStuck "$REPORTSUBJECT" "$REPORTBODY"
fi


# Send an email if necessary
checkForEmailSending


