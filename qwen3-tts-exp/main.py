import os
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

print("Loading model...")
model = Qwen3TTSModel.from_pretrained(
    "./Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)
print("Model loaded.")

ref_audio = "./samples/ATR_b101_020.wav"
ref_text  = "さっき、海の中で出逢った時から、そんな気がしていました。やっぱりそうだったんですね。"

def main():
    wavs, sr = model.generate_voice_clone(
        text="おはようございます、なつきさん。",
        language="japanese",
        ref_audio=ref_audio,
        ref_text=ref_text,
    )
    print("Sample Rate:", sr, "Hz")
    os.makedirs("dist", exist_ok=True)
    sf.write("dist/ATR_main.wav", wavs[0], sr)

if __name__ == "__main__":
    main()
