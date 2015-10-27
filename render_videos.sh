#!/bin/bash

trap "exit 1" 2 # catch SIGINT

dir=$(dirname "$0")
cd "$dir"

outroot="output/muserc_sav_pre"

if [ ! -d "${outroot}" ]; then
  mkdir "${outroot}"
fi

# setup log
output="output/muserc_sa_pre/muserc_sav"

if [ ! -d "${output}" ]; then
  mkdir "${output}"
fi

sharpend_opt=("-filter:v" "unsharp=5:5:1.5:5:5:1.0,eq=contrast=3.2:brightness=0.9:gamma=1.8:gamma_g=0.95:saturation=1.1" "-c:v" "libx264" "-crf" "0" "-preset" "veryslow")
compressed_opt=("-crf" "18")
realtime_opt=("-r" "60" "-preset" "slow" "-crf" "16" "-filter:v" "setpts=0.0125*PTS")
all_opts=("-pix_fmt" "yuv420p" "-y")

##################################################################
# Process Video 1                                                #
##################################################################

input1="data/muserc_sensor_audio_video_raw/G120002_001_001.mp4"

echo "processing $input1..."
file="`basename $input1`"
base="${output}/amateur_51_m_vib"

sharpened1="${base}_sharpened.mp4"
compressed1="${base}_compressed.mp4"
realtime1="${base}_compressed_realtime_60fps.mp4"

# change contrast and use 420p video format
ffmpeg -i "$input1" "${sharpend_opt[@]}" "${all_opts[@]}" "$sharpened1"

# write lossy mp4 version
ffmpeg -i "$sharpened1" "${compressed_opt[@]}" "${all_opts[@]}" "$compressed1"

# write realtime version
ffmpeg -i "$compressed1" "${realtime_opt[@]}" "${all_opts[@]}" "$realtime1"

# mux audio to 60fps realtime video

# ##################################################################
# # Process Video 2                                                #
# ##################################################################

input2="data/muserc_sensor_audio_video_raw/G120002_002_001.mp4"

echo "processing $input2..."
file="`basename $input2`"
base="${output}/pro_51_f_vib"

sharpened2="${base}_sharpened.mp4"
compressed2="${base}_compressed.mp4"
realtime2="${base}_compressed_realtime_60fps.mp4"

# change contrast and use 420p video format
ffmpeg -i "$input2" "${sharpend_opt[@]}" "${all_opts[@]}" "$sharpened2"

# write lossy mp4 version
ffmpeg -i "$sharpened2" "${compressed_opt[@]}" "${all_opts[@]}" "$compressed2"

# write realtime version
ffmpeg -i "$compressed2" "${realtime_opt[@]}" "${all_opts[@]}" "$realtime2"

# mux audio to 60fps realtime video
