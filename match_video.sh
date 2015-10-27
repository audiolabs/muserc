#!/bin/sh

# run match.py for all video files in the `data' directory

flags=""

trap "exit 1" 2 # catch SIGINT

if [ -n "$1" ]; then
  echo "usage: $0"
  exit 1
fi

dir=$(dirname "$0")
cd "$dir"

outroot="output/muserc_sav_pre"

if [ ! -d "${outroot}" ]; then
  mkdir "${outroot}"
fi

# setup log
outdir="output/muserc_sav_pre/muserc_sav"

if [ ! -d "${outdir}" ]; then
  mkdir "${outdir}"
fi

log_base="$outdir/match_video"
log="${log_base}.log"
i=0

while [ -e "$log" ]; do
  i="`expr $i + 1`"
  log="${log_base}_${i}.log"
done

touch "$log"


# video 1
audio="data/muserc_sensor_audio_video_raw/data_video1_audio"
sync="data/muserc_sensor_audio_video_raw/data_video1_sync"
sensor="data/muserc_sensor_audio_video_raw/data_video1_sensor"
cutlist="data/muserc_sensor_audio_video_raw/data_video1_cutlist"

title="amateur_51_m_vib"

echo "$title ..."

echo "./match.py -v $flags \"${audio}\" \"${sync}\" \"${sensor}\" \"$title\" \"${outdir}\" -c \"${cutlist}\" >>$log 2>>$log" >>$log

./match.py -v $flags "${audio}" "${sync}" "${sensor}" "$title" "$outdir" -c "${cutlist}" >>$log 2>>$log


# video 2
audio="data/muserc_sensor_audio_video_raw/data_video2_audio"
sync="data/muserc_sensor_audio_video_raw/data_video2_sync"
sensor="data/muserc_sensor_audio_video_raw/data_video2_sensor"
cutlist="data/muserc_sensor_audio_video_raw/data_video2_cutlist"

title="pro_51_f_vib"

echo "$title ..."

echo "./match.py -v $flags \"${audio}\" \"${sync}\" \"${sensor}\" \"$title\" \"${outdir}\" -c \"${cutlist}\" >>$log 2>>$log" >>$log

./match.py -v $flags "${audio}" "${sync}" "${sensor}" "$title" "$outdir" -c "${cutlist}" >>$log 2>>$log
