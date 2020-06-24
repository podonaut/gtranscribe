#!/usr/bin/env python
import os
import sys
import configparser
import wave
from pydub import AudioSegment
from datetime import datetime
from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


class Transcribe:

    config = configparser.ConfigParser()
    config.read('gcloud.ini')   
    bucket_name = config['CREDENTIALS']['BUCKET_NAME']
    jsonfile = config['CREDENTIALS']['JSON']

    supported = [
        "wav",
        "mp3",
        "ogg",
    ]

    def __init__(self, audiofile):

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.jsonfile

        self.audiofile = audiofile
        self.audioext = self.audiofile.split(".")[1]
        self.wavfile = os.path.basename(self.audiofile) + ".wav"
        self.transcriptfile = f"transcript/{os.path.basename(self.audiofile)}.txt"
        if not os.path.isdir("transcript"):
            os.mkdir("transcript")
        self.frame_rate = None
        self.channels = None
        if not self.audioext in self.supported:
            raise Exception(f"Unknown Ext: {self.audioext}")
        self.toWav()

    def toWav(self):
        if not os.path.isfile(self.wavfile):
            if self.audioext == "wav":
                return
            elif self.audioext == "mp3":
                sound = AudioSegment.from_mp3(self.audiofile)
            elif self.audioext == "ogg":
                sound = AudioSegment.from_ogg(self.audiofile)
            elif self.audioext == "flac":
                sound = AudioSegment.from_flac(self.audiofile)
            newsound = sound.set_channels(1)
            print(f"Converting {self.audiofile} to {self.wavfile}")
            newsound.export(self.wavfile, format="wav")

        with wave.open(self.wavfile, "rb") as wave_file:
            self.frame_rate = wave_file.getframerate()
            self.channels = wave_file.getnchannels()
            if not 1 == self.channels:
                raise Exception("There can only be one channel in wav file")

    def uploadBlob(self):
        """Uploads a file to the bucket."""
        self.destination_name = self.wavfile
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(self.bucket_name)
        self.blob = bucket.blob(self.destination_name)
        self.blob.upload_from_filename(self.wavfile)
        os.unlink(self.wavfile)

    def deleteBlob(self):
        """Deletes a file from the bucket."""
        self.blob.delete()

    def transcribeAudio(self):
        self.gcs_uri = f"gs://{self.bucket_name}/{self.destination_name}"

        t0 = datetime.now()
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri=self.gcs_uri)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.frame_rate,
            language_code="en-US",
        )

        # Detects speech in the audio file
        operation = client.long_running_recognize(config, audio)
        response = operation.result(timeout=10000)
        t1 = datetime.now()

        time_taken = t1 - t0
        print(f"Translation time: {time_taken}")

        print(response)

        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        print(transcript)
        f = open(self.transcriptfile, "w")
        f.writelines(transcript)
        f.close()


def main(audiofile):
    t = Transcribe(audiofile)
    t.uploadBlob()
    t.transcribeAudio()
    t.deleteBlob()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        audiofile = sys.argv[1]
    else:
        audiofile = "audio/magic-stereo.mp3"

    main(audiofile)
