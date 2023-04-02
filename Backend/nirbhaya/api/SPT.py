from transformers import Wav2Vec2Processor, Wav2Vec2ConformerForCTC
import torch
# from datasets import load_dataset
import librosa
import jellyfish
from django.conf import settings


def get_speech_to_text(model, processor, audio_path):
    data, sample_rate = librosa.load(audio_path, sr=16000)
    input_values = processor(data, return_tensors="pt", padding="longest").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    return transcription

# make the percentage match between two strings here
def get_percentage_match(transcription, text):
    return jellyfish.jaro_distance(transcription, text)

def main():
    # load model and processor
    processor = Wav2Vec2Processor.from_pretrained(f"{settings.BASE_URL}/api/SPT_model")
    model = Wav2Vec2ConformerForCTC.from_pretrained(f"{settings.BASE_URL}/api/SPT_model")
    transcription = get_speech_to_text(model, processor, audio_path=f"{settings.BASE_URL}/api/SPT_model/test_audios/03-01-01-01-01-01-01.wav")
    print(transcription)
    text = "KIDS ARE TALKING BY THE DOOR"
    print(get_percentage_match(transcription[0], text))

if __name__ == "__main__":
    main()