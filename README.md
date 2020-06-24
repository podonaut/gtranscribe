# gTrancript

I found this article on medium about using the [google speech to text API](https://towardsdatascience.com/how-to-use-google-speech-to-text-api-to-transcribe-long-audio-files-1c886f4eb3e9).

As a python coder this was a good first start, but was not in a state that I could just use it.

Please read the original article, for the why, this is just the how.

So how do you convert the speech an audio file (mp3, ogg, wav) to text? I have uploaded all you need to this git repository
    
    https://github.com/podonaut/gtranscribe
    
## gTrancribe
To get code:

    git clone https://github.com/podonaut/gtranscribe
    
I recommend using virtualenv/venv to setup your own local copy of python:

    virtualenv -p python3 ~/.venv/gtranscribe
    source ~/.venv/gtranscribe/bin/activate
    
Then you will need to install the dependent python modules, these are all contained in the requirements.txt file in the directory that comes from the repo.

    pip install -r requirements.txt
    
I was able to get this working under native windows and linux, not cygwin.

## Google cloud account.

As per the original article you will need a [google cloud platform account](https://console.cloud.google.com/).

Once set up you will need to [set up a _"bucket"_](https://cloud.google.com/storage/docs/creating-buckets), this is an area where you can upload data to on google servers.

You will [need setup a <credentials>.json](https://cloud.google.com/docs/authentication/getting-started). This is used by the python script to authenticate against the google servers and allow you to upload the audio file to the server and then call the transcription services.

In my project I have called the bucket "throat", and I have included an example json file, gcloud-123011d921d1.json, this is a dummy file, to see what one looks like, you can't use it (well you can, but it won't work!)

Google charges you for the pleasure, but at the time of writing 100 minutes of transcription per months is free. The script when it finishes removes the audio file from the server. If you exit prematurely you may have left it on the server. It is no harm to have a look when you are done and make sure the bucket is empty or files.

Once you have the bucket name and json file, edit the gcloud.ini file accordingly (no quotes):

    [CREDENTIALS]
    BUCKET_NAME = throat
    JSON = gcloud-123011d921d1.json

## FFMPEG

The python script calls ffmpeg under the hood. Make sure it is installed on you machine and in your path:

[How to install ffmpeg](https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/)

## Transcribe

You should now be setup. I have included a few audio files in the audio directory. It is [Thackery Binx](https://disney.fandom.com/wiki/Thackery_Binx) from the movie [Hocus Pocus](https://disney.fandom.com/wiki/Hocus_Pocus) saying the phrase, _"it's protected by magic"_.

_Bonus points if any one can figure out why that snippet of audio is being used._

To call the script it is:

    transcribe_audio.py <audiofile>

Or in this case you can use the one in the repo:

    transcribe_audio.py audio\magic-mono.mp3

In the background, it converts it to a single channel wav file, uploads it to google, translates it, prints the translation to the script and writes it to a text file in the transcript directory and finally deletes the wav file from the google server.

Sample output:

    Converting audio\magic-mono.mp3 to magic-mono.mp3.wav
    Translation time: 0:00:03.248001
        results {
            alternatives {
                transcript: 'it\'s protected by Magic'
                confidence: 0.9515093564987183
            }
        }
    it's protected by Magic

That's it, its working!

Get your own audio file and try it, at the moment it only supports mp3, ogg and wav files.

## Conclusions
This post is just for setup. The efficiency of google speech to text is not great I will detail it in another post. I suspect it is because I have an Irish accent but the AI (deep learning) was trained mainly on American accents.
