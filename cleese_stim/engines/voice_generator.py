#!/usr/bin/env python
# -*- coding: utf-8 -*-

import azure.cognitiveservices.speech as speechsdk
from cleese_stim.engines.engine import Engine
import numpy as np
import sys

class VoiceGenerator(Engine):

  @staticmethod
  def process(text_data, config):

    key = config["key"]
    region = config["region"]
    output_file = config["output"]
    voice = config["voice"]
    language = config["language"]
    features = config["features"]

    base_template = '<prosody FEATURE > WORD </prosody>'
    ssml_template = '''
      <speak 
        xmlns="http://www.w3.org/2001/10/synthesis" 
        xmlns:mstts="http://www.w3.org/2001/mstts" 
        xmlns:emo="http://www.w3.org/2009/10/emotionml" 
        version="1.0" xml:lang="LANGUAGE"
        >
        <voice name="VOICE">
          <mstts:express-as style="Neutral" >
            TEXT
          </mstts:express-as>
        </voice>
      </speak>
    '''

    def createRandomValues(feature_config, num_words):
      # random BPF values
      # center is set as per azure reccomended values
      values = np.random.normal(0, feature_config['std'], num_words)

      # eliminate far samples (trunc factor)
      # and replace them by new random values
      for i, value in enumerate(values):
          while np.abs(value) > (feature_config['std'] * feature_config['trunc']):
              values[i] = np.random.normal(0, feature_config['std'], 1)

      return(values)

    text = open(text_data, "r").read()
    text_list = text.split(' ')
    ssml = []
    random_feature_values = {}

    for feature in features:
      if feature == 'pitch':
        random_feature_values['pitch'] = createRandomValues(config['pitch'] ,len(text_list))
      if feature == 'speed':
        random_feature_values['speed'] = createRandomValues(config['speed'] ,len(text_list))

    for i,word in enumerate(text_list) :
      template = base_template
      ######## do we also want loudness? pauses? ##########
      ##                                                 ##
      #####################################################
      for feature in features :
        if feature == 'pitch' :
          if random_feature_values["pitch"][i] > 0 :
            template = template.replace("FEATURE", f'pitch="+{round(random_feature_values["pitch"][i])}%" FEATURE')
          else:
            template = template.replace("FEATURE", f'pitch="{round(random_feature_values["pitch"][i])}%" FEATURE')
        elif feature == 'speed' :
          if random_feature_values["speed"][i] > 0 :
            template = template.replace("FEATURE", f'rate="+{round(random_feature_values["speed"][i])}%" FEATURE')
          else:
            template = template.replace("FEATURE", f'rate="{round(random_feature_values["speed"][i])}%" FEATURE')
        else :
          print("incorrect feature input : please supply any combination of 'speed', 'pitch'")
          sys.exit(1)

      # remove the FEATURE tag for templating
      template = template.replace(" FEATURE", '')
      template = template.replace("WORD", word)
      ssml.append(template)

    ssml_input = ssml_template.replace("LANGUAGE", language)
    ssml_input = ssml_input.replace("VOICE", voice)
    ssml_input = ssml_input.replace("TEXT", '\n'.join(ssml))

    #Run TTS synthesis in Microsoft Azure, requires account with key
    try:
      speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
      audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

      speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

      result = speech_synthesizer.speak_ssml_async(ssml_input).get()

      if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
          print("Speech synthesized for text [{}]".format(text))
      elif result.reason == speechsdk.ResultReason.Canceled:
          cancellation_details = result.cancellation_details
          print("Speech synthesis canceled: {}".format(cancellation_details.reason))
          if cancellation_details.reason == speechsdk.CancellationReason.Error:
              if cancellation_details.error_details:
                  print("Error details: {}".format(cancellation_details.error_details))
                  print("Did you set the speech resource key and region values?")

      stream = speechsdk.AudioDataStream(result)
      stream.save_to_wav_file(output_file)
    except Exception as e:
      print(e)

    return(stream, random_feature_values)
