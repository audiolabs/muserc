<img src="https://cloud.githubusercontent.com/assets/72940/10666256/c0cd8e08-78d0-11e5-8cdb-346046b5fcff.jpg" width="480">
# MUSERC Pre-Processing

Pre-process the raw MUSERC dataset so that 

* Audio, video and sensor data is cut, cleaned up and compressed for easier and faster handling

## Audio 

* recorded using AKG C414 
* Samplingrate 48000 Hz
* Raw data: 24bit uncompressed mono PCM
* Pre-Processed Data: 16 bit uncompressed mono PCM

## Video 

* High speed camera (2000 fps)
* Focusing on the string to extract the movement pattern
* Resolution 1024x768
* Raw data: H264 lossless mode
* Pre-Processed Data: H264 lossy compression

## Sensors

* To measure the finger position, we used a linear membrane potentiometer.
* Recorded using 12bit D/A at 750 Hz.

## Howto run the pre-processing

* install requirements ```pip install -r requirements.txt````
* for video processing install ffmpeg
* run ```make```

## Authors

* [Fabian-Robert Stöter](https://www.audiolabs-erlangen.de/fau/assistant/stoeter), [International Audio Laboratories Erlangen](https://www.audiolabs-erlangen.de)
* Michael Müller, TU Graz
* [Bernd Edler](https://www.audiolabs-erlangen.de/fau/professor/edler),[International Audio Laboratories Erlangen](https://www.audiolabs-erlangen.de)

## Licence

MUSERC is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/). If you use this dataset in your academic research, please cite our paper:

[Fabian-Robert Stöter, Michael Müller, and Bernd Edler. 2015. Multi-Sensor Cello Recordings for Instantaneous Frequency Estimation. In Proceedings of the 23rd Annual ACM Conference on Multimedia Conference (MM '15). ACM, New York, NY, USA, 995-998.](http://dl.acm.org/citation.cfm?id=2806384)
