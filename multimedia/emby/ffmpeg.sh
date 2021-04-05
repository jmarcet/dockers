#!/bin/sh

if echo $@ | grep -q h264_vaapi; then
	ARGS=$@
else
	ARGS="$( echo $@ | sed -E -e 's,c:v:0 h264 -user,c:v:0 h264 -hwaccel:v:0 vaapi -hwaccel_device:v:0 /dev/dri/renderD128 -hwaccel_output_format:v:0 vaapi -user,' -e 's: libx264: h264_vaapi:' -e 's,filter_complex [^ ]+ ,filter_complex [0:0]deinterlace_vaapi@f1[f1_out0] ,' -e 's, -pix_fmt:v:0 .+ -profile, -profile,' -e 's, -x264opts:v:0 .+ -c:a:0, -c:a:0,' )"
fi
ffmpeg $ARGS
