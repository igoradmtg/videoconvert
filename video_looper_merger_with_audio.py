import argparse
import os
import subprocess
import glob
import tempfile
import shutil
from dotenv import load_dotenv

CONFIG_FILE = "video_looper_merger_with_audio.env"

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
        print(f"Файл конфигурации {CONFIG_FILE} не найден, используются параметры по умолчанию")

def main():
    load_config()
    
    parser = argparse.ArgumentParser(description="Объединение видеофайлов с аудиодорожкой")
    parser.add_argument("--input-dir", 
                      default=os.getenv("INPUT_DIR"), 
                      help=f"Директория с MP4 файлами (по умолчанию из {CONFIG_FILE})")
    parser.add_argument("--output", 
                      default=os.getenv("OUTPUT", "output.mp4"), 
                      help=f"Имя выходного файла (по умолчанию из {CONFIG_FILE})")
    parser.add_argument("--audio", 
                      default=os.getenv("AUDIO"), 
                      help=f"Путь к аудиофайлу (MP3) (по умолчанию из {CONFIG_FILE})")
    parser.add_argument("--video-loops", 
                      type=int, 
                      default=int(os.getenv("VIDEO_LOOPS", 1)), 
                      help=f"Количество зацикливаний видео (по умолчанию из {CONFIG_FILE})")
    parser.add_argument("--audio-loops", 
                      type=int, 
                      default=int(os.getenv("AUDIO_LOOPS", 1)), 
                      help=f"Количество зацикливаний аудио (по умолчанию из {CONFIG_FILE})")
    
    args = parser.parse_args()

    if not args.input_dir:
        print(f"Ошибка: необходимо указать --input-dir или задать INPUT_DIR в {CONFIG_FILE}")
        return

    if not check_ffmpeg():
        print("Ошибка: ffmpeg не установлен или не доступен в системе")
        return

    video_files = glob.glob(os.path.join(args.input_dir, "*.mp4"))
    if not video_files:
        print(f"Не найдено MP4 файлов в указанной директории: {args.input_dir}")
        return

    temp_dir = tempfile.mkdtemp()
    try:
        file_list = create_file_list(video_files, args.video_loops, temp_dir)
        temp_video = os.path.join(temp_dir, "temp.mp4")
        
        concat_cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", file_list,
            "-c", "copy",
            "-y", temp_video
        ]
        subprocess.run(concat_cmd, check=True)

        if args.audio and os.path.isfile(args.audio):
            final_cmd = [
                "ffmpeg",
                "-i", temp_video,
                "-stream_loop", str(args.audio_loops - 1),  # FFmpeg считает повторы иначе
                "-i", args.audio,
                "-c:v", "copy",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                "-y", args.output
            ]
            subprocess.run(final_cmd, check=True)
        else:
            shutil.copy(temp_video, args.output)
            print("Аудио не добавлено")

        print(f"Успешно создан файл: {args.output}")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обработке видео: {str(e)}")
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()