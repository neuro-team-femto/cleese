#!/usr/bin/env python
# -*- coding: utf-8 -*-

import azure.cognitiveservices.speech as speechsdk
from cleese_stim.engines.engine import Engine

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

    text = open(text_data, "r").read()
    text_list = text.split(' ')
    pitch_list = []
    rate_list = []
    ssml = []

    ###########Randomization of the rate and pitch here ##################
    ##                                                                  ##
    ######################################################################

    for i,word in enumerate(text_list) :
      template = base_template
      ######## do we also want loudness? pauses? ##########
      ##                                                 ##
      #####################################################
      for feature in features :
        if feature == 'pitch' :
          template = template.replace("FEATURE", f'pitch="{pitch_list[i]}" FEATURE')
        elif feature == 'speed' :
          template = template.replace("FEATURE", f'rate="{rate_list[i]}" FEATURE')
        else :
          print("incorrect feature input : please supply any combination of 'speed', 'pitch'")
          exit(1)

      # remove the FEATURE tag for templating
      template = template.replace(" FEATURE", '')
      template = template.replace("WORD", word)
      ssml.append(template)

    ssml_template = ssml_template.replace("LANGUAGE", language)
    ssml_template = ssml_template.replace("VOICE", voice)
    ssml_template = ssml_template.replace("TEXT", '\n'.join(ssml))

    #Run TTS synthesis in Microsoft Azure, requires account with key
    try:
      speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
      audio_config = speechsdk.audio.AudioOutputConfig(filename = output_file)

      synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)

      result = synthesizer.speak_ssml_async(ssml).get()

      if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text_data))
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
