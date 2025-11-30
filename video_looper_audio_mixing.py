import argparse
import os
import subprocess
import glob
import tempfile
import shutil
from dotenv import load_dotenv

CONFIG_FILE = "video_looper_audio_mixing.env"

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_file_list(video_files, loops, temp_dir):
    file_list_path = os.path.join(temp_dir, "input.txt")
    with open(file_list_path, "w") as f:
        for _ in range(loops):
            for file in video_files:
                f.write(f"file '{os.path.abspath(file)}'\n")
    return file_list_path

def load_config():
    if os.path.exists(CONFIG_FILE):
        load_dotenv(CONFIG_FILE)
        print(f"Загружена конфигурация из {CONFIG_FILE}")
    else:
        print(f"Файл конфигурации {CONFIG_FILE} не найден")

def main():
    load_config()
    
    parser = argparse.ArgumentParser(description="Объединение видео с микшированием аудио")
    parser.add_argument("--input-dir", default=os.getenv("INPUT_DIR"))
    parser.add_argument("--output", default=os.getenv("OUTPUT", "output.mp4"))
    parser.add_argument("--audio", default=os.getenv("AUDIO"))
    parser.add_argument("--video-loops", type=int, default=int(os.getenv("VIDEO_LOOPS", 1)))
    parser.add_argument("--audio-loops", type=int, default=int(os.getenv("AUDIO_LOOPS", 1)))
    parser.add_argument("--mix-audio", default=os.getenv("MIX_AUDIO"))
    parser.add_argument("--mix-loops", type=int, default=int(os.getenv("MIX_LOOPS", 1)))
    parser.add_argument("--main-volume", type=float, default=float(os.getenv("MAIN_VOLUME", 1.0)))
    parser.add_argument("--mix-volume", type=float, default=float(os.getenv("MIX_VOLUME", 1.0)))
    
    args = parser.parse_args()

    if not args.input_dir:
        print("Ошибка: необходимо указать --input-dir")
        return

    # Сборка аудио компонентов
    audio_inputs = []
    audio_filters = []
    audio_index = 1  # Счетчик аудио потоков
    
    # Обработка основного аудио
    if args.audio and os.path.isfile(args.audio):
        audio_inputs.extend([
            "-stream_loop", str(args.audio_loops - 1),
            "-i", args.audio
        ])
        audio_filters.append(
            f"[{audio_index}:a]aformat=channel_layouts=stereo:sample_fmts=s16:sample_rates=44100,"
            f"volume={args.main_volume}[a{audio_index}]"
        )
        audio_index += 1
    
    # Обработка дополнительного аудио
    if args.mix_audio and os.path.isfile(args.mix_audio):
        audio_inputs.extend([
            "-stream_loop", str(args.mix_loops - 1),
            "-i", args.mix_audio
        ])
        audio_filters.append(
            f"[{audio_index}:a]aformat=channel_layouts=stereo:sample_fmts=s16:sample_rates=44100,"
            f"volume={args.mix_volume}[a{audio_index}]"
        )
        audio_index += 1

    temp_dir = tempfile.mkdtemp()
    try:
        # Создание временного видео
        video_files = glob.glob(os.path.join(args.input_dir, "*.mp4"))
        file_list = create_file_list(video_files, args.video_loops, temp_dir)
        temp_video = os.path.join(temp_dir, "temp.mp4")
        
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", file_list,
            "-c", "copy", "-y", temp_video
        ], check=True)

        # Сборка финальной команды
        cmd = ["ffmpeg", "-i", temp_video] + audio_inputs
        
        if audio_filters:
            # Формируем цепочку фильтров
            filter_chain = []
            filter_labels = []
            
            for i, filt in enumerate(audio_filters, 1):
                filter_chain.append(filt)
                filter_labels.append(f"[a{i}]")
            
            if len(audio_filters) > 1:
                filter_chain.append(f"{''.join(filter_labels)}amix=inputs={len(audio_filters)}:duration=longest[aout]")
            else:
                filter_chain[0] = filter_chain[0].replace(f"[a1}]", "[aout]")
            
            cmd += [
                "-filter_complex", ";".join(filter_chain),
                "-map", "0:v:0",
                "-map", "[aout]",
                "-c:v", "copy",
                "-y", args.output
            ]
        else:
            cmd += ["-c", "copy", "-y", args.output]

        subprocess.run(cmd, check=True)
        print(f"Файл создан: {args.output}")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка обработки: {str(e)}")
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()