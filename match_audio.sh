#!/bin/sh

# run match.py for all audio files in the `data' directory

flags=""

pids=()

function clean_exit
{
  echo "caught SIGINT, stopping processes..."

  for pid in ${pids[@]}; do
    kill $pid 2>/dev/null
  done

  exit 1
}

trap "clean_exit" 2 # catch SIGINT

if [ -n "$1" ]; then
  echo "usage: $0"
  exit 1
fi

dir=$(dirname "$0")
cd "$dir"

# setup log
outroot="output/muserc_sa_pre"

if [ ! -d "${outroot}" ]; then
  mkdir "${outroot}"
fi

# setup log
outdir="output/muserc_sa_pre/muserc_sa"

if [ ! -d "${outdir}" ]; then
  mkdir "${outdir}"
fi


log_base="$outdir/match_audio"
log="${log_base}.log"
i=0

while [ -e "$log" ]; do
  i="`expr $i + 1`"
  log="${log_base}_${i}.log"
done

touch "$log"

for f in data/muserc_sensor_audio_raw/data_*_audio ; do

  # videos are processed in match_video.sh
  grep -q "video" <<< $f && continue

  base="${f%%_audio}"
  file="`basename $base`"
  tone="$(echo $file | sed 's/.*_//')"
  exp="$(echo $file | sed 's/data_\([^_]*\)_.*/\1/')"

  case "$tone" in
    "d3")
        midi="50"
        ;;
    "dsharp3")
        midi="51"
        ;;
    "e3")
        midi="52"
        ;;
    "f3")
        midi="53"
        ;;
    "b3")
        midi="59"
        ;;
    "c4")
        midi="60"
        ;;
    "csharp4")
        midi="61"
        ;;
    *)
      echo "Error: unrecognized input note in file name $file. Aborting..." >>$log
      echo "Error: unrecognized input note in file name $file. Aborting..."
      exit 1
  esac

  title="${exp}_${midi}"
  mlog="${log%.log}_$title.log"
  cutlist="-c ${base}_cutlist"

  echo "starting $title ..."

  echo "./match.py -v \"${base}_audio\" \"${base}_sync\" \"${base}_sensor\" \"$title\" \"$outdir\" $cutlist $flags >>$mlog 2>>$mlog &" >>$log

  ./match.py -v "${base}_audio" "${base}_sync" "${base}_sensor" "$title" "$outdir" $cutlist $flags >>$mlog 2>>$mlog &

  pids+=($!)

done

echo "waiting for processes to finish..."

for pid in ${pids[@]}; do
  wait $pid
done
