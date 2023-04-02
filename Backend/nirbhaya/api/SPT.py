import torch
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification, Wav2Vec2Processor, Wav2Vec2ConformerForCTC
import librosa
import jellyfish
# from django.conf import settings


def speech_file_to_array_fn(path, sampling_rate):
    speech_array, _sampling_rate = torchaudio.load(path)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech = resampler(speech_array).squeeze().numpy()
    return speech

def predict(path, sampling_rate, feature_extractor, device, model, config):
    speech = speech_file_to_array_fn(path, sampling_rate)
    inputs = feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
    inputs = {key: inputs[key].to(device) for key in inputs}
    with torch.no_grad():
        logits = model(**inputs).logits
    scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    outputs = [{"Emotion": config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
    return outputs

def get_speech_to_text(model, processor, audio_path):
    data, sample_rate = librosa.load(audio_path, sr=16000)
    input_values = processor(data, return_tensors="pt", padding="longest").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    return transcription

# def get_percentage_match(transcription, text):
#     return jellyfish.damerau_levenshtein_distance(transcription, text)

def get_sos_status(transcription, key_phrase):
    ct = 0
    for words in key_phrase.split(" "):
        # print(type(words))
        if transcription[0].find(words) != -1:
            ct = ct + 1
    if ct == 3:
        sos = 1
    else:
        sos = 0
    return sos

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SPT_MODEL = "C:\\Users\\taaha\\OneDrive\\Desktop\\Nirbhaya-Women4Women\\Backend\\nirbhaya\\api\\SPT_model"
# SPT_MODEL = "D:/kaggle_practice/KJSCE_hack/SPT_model"
model_name_or_path = "C:\\Users\\taaha\\OneDrive\\Desktop\\Nirbhaya-Women4Women\\Backend\\nirbhaya\\api\\SER_model"
# model_name_or_path = "D:\kaggle_practice\KJSCE_hack\SER_model"
config = AutoConfig.from_pretrained(model_name_or_path)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name_or_path)
sampling_rate = feature_extractor.sampling_rate
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name_or_path).to(device)
processor = Wav2Vec2Processor.from_pretrained(SPT_MODEL)
model_SPT = Wav2Vec2ConformerForCTC.from_pretrained(SPT_MODEL)

def main():
    path = "C:\\Users\\taaha\\OneDrive\\Desktop\\Nirbhaya-Women4Women\\Backend\\nirbhaya\\api\\SPT_model/test_audios/test_10.wav"
    outputs = predict(path, sampling_rate, feature_extractor, device = device, model = model, config = config)
    transcription = get_speech_to_text(model_SPT, processor, audio_path=path)
    key_phrase = "DOGS DOOR SITTING"
    status = get_sos_status(transcription, key_phrase)
    max_score = 0
    emotion = ""
    for i in outputs:
        if float(i['Score'][:-1]) > max_score:
            max_score = float(i['Score'][:-1])
            emotion = i['Emotion']
    if emotion in ['disgust', 'fear', 'sadness']:
        emotion = 'negative'
    elif emotion == 'neutral':
        emotion = 'neutral'
    else:
        emotion = 'positive'
    
    if emotion == 'negative' or status == 1:
        sos = True
    else:
        sos = False

    return sos

if __name__ == "__main__":
    outputs = main()
    print(outputs)


