.PHONY: fetchdata

URLBASE=https://www.audiolabs-erlangen.de/content/resources/muserc
FILES=\
	muserc_sensor_audio_raw.tar.gz.md5 \
	muserc_sensor_audio_raw.tar.gz \
	muserc_sensor_audio_video_raw.tar.gz.md5 \
	muserc_sensor_audio_video_raw.tar.gz

%.tar.gz %.tar.gz.md5:
	curl -LO "${URLBASE}/$@"

fetchdata: ${FILES}
	mkdir -p muserc_sensor_audio_raw
	tar xvzf muserc_sensor_audio_raw.tar.gz -C muserc_sensor_audio_raw

	mkdir -p muserc_sensor_audio_video_raw
	tar xvzf muserc_sensor_audio_video_raw.tar.gz -C muserc_sensor_audio_video_raw
