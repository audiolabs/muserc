.PHONY: install checkdata rendervideos audiosensorset audiovideosensorset

all:
	$(MAKE) install
	$(MAKE) fetchdata
	$(MAKE) rendervideos
	$(MAKE) sa
	$(MAKE) sav

install:
	pip install -r requirements.txt

fetchdata:
	$(MAKE) -C data fetchdata

rendervideos:
	test ! -f "output/muserc_sav_pre/muserc_sav/pro_51_f_vib_compressed_realtime_60fps.mp4"
	sh render_videos.sh

# create sensor/audio dataset
sa:
	sh match_audio.sh
	./gen_yaml.py output/muserc_sa_pre/muserc_sa -o output/muserc_sa_pre/muserc_sa.yaml
	cp data/DATA-LICENSE.txt output/muserc_sa_pre/license.txt
	find ./output/ -name '*.DS_Store' -type f -delete
	find ./output/ -name '*.log' -type f -delete
	tar -czvf output/muserc_sa_pre.tar.gz -C output/muserc_sa_pre .

# create sensor/audio/video dataset
sav:
	sh match_video.sh
	./gen_yaml.py -v output/muserc_sav_pre/muserc_sav -o output/muserc_sav_pre/muserc_sav.yaml
	cp data/DATA-LICENSE.txt output/muserc_sav_pre/license.txt
	find ./output/ -name '*.DS_Store' -type f -delete
	find ./output/ -name '*.log' -type f -delete
	tar -czvf output/muserc_sav_pre.tar.gz -C output/muserc_sav_pre .
