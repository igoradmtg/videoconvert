#!/usr/bin/env python
# Указывает, что скрипт должен выполняться интерпретатором Python

# -*- coding: utf-8 -*-
# Задает кодировку файла как UTF-8 для поддержки русских символов

# Конвертация DVD to mkv
# Комментарий с кратким описанием цели скрипта

# ffmpeg -fflags +genpts -analyzeduration 100M -probesize 100M -i 00001.vob -codec:v copy -codec:a copy -codec:s copy 00001.mkv
# Пример команды ffmpeg для конвертации VOB в MKV (записан как комментарий)

import os
# Импортирует модуль os для работы с файловой системой

dirFilesInput = r"W:\001\Video_avi"
# Задает путь к входной папке с исходными видеофайлами

dirFilesOutput = r"W:\001\Video_mp4"
# Задает путь к выходной папке для сконвертированных файлов

#dirFiles = r"w:\upl1_teach"
# Зачеркнутый путь к другой папке (не используется)

numSegments = 30  # Количество сегментов из видеоклипа
# Задает количество сегментов для разделения видео (не используется в коде)

segmentDuration = 10  # Длительность сегмента в секундах
# Задает длительность одного сегмента в секундах (не используется в коде)

segmentDuration = 2  # Длительность сегмента в секундах
# Переопределяет длительность сегмента на 2 секунды (не используется в коде)

def replace_all(text, dic):
    # Определяет функцию replace_all для замены подстрок в тексте по словарю
    for i, j in dic.items():
        # Перебирает пары ключ-значение из словаря
        text = text.replace(i, j)
        # Заменяет в тексте все вхождения ключа на значение
    return text
    # Возвращает измененный текст

def main():
    # Определяет главную функцию main для выполнения основной логики скрипта
    files = []
    # Создает пустой список для хранения путей к видеофайлам
    # r=root, d=directories, f = files
    # Комментарий, поясняющий переменные os.walk
    for r, d, f in os.walk(dirFilesInput):
        # Перебирает все файлы и папки в dirFilesInput рекурсивно
        #print(f"{r} {d} {f}")
        # Зачеркнутая строка для отладки (выводит пути, папки и файлы)
        if 'thumb' in r:
            # Проверяет, есть ли подстрока 'thumb' в пути к папке
            continue
            # Пропускает папки, содержащие 'thumb'
        for file in f:
            # Перебирает файлы в текущей папке
            file_lower = str(file).lower()
            # Преобразует имя файла в нижний регистр для проверки расширения
            if ('.avi' in file_lower) or ('.wmv' in file_lower) or ('.m4v' in file_lower) or ('.mpg' in file_lower) or ('.avi' in file_lower) or ('.wmv' in file_lower) or ('.mov' in file_lower) or ('.divx' in file_lower) or ('.webm' in file_lower) or ('.vob' in file_lower) or ('.mts' in file_lower) or ('.mpeg' in file_lower):
                # Проверяет, имеет ли файл одно из указанных видео-расширений
                files.append(os.path.join(r, file))
                # Добавляет полный путь к файлу в список files
    for fileName in files:
        # Перебирает все найденные видеофайлы
        fileSplit = os.path.split(fileName)
        # Разделяет полный путь на директорию и имя файла
        fileBase = fileSplit[-1]
        # Получает имя файла (без директории)
        extension_map = {".avi":".mp4",".wmv":".mkv",".m4v":".mp4",".mpg":".mkv",".mov":".mkv",".divx":".mkv",".webm":".mkv",".vob":".mkv",".mts":".mp4",".mpeg":".mp4"}
        # Создает словарь соответствия старых расширений новым
        file_ext = os.path.splitext(fileBase)[1].lower()
        # Получает расширение файла в нижнем регистре
        new_ext = extension_map.get(file_ext, file_ext)
        # Получает новое расширение из словаря, если есть, иначе оставляет старое
        fileBase = os.path.splitext(fileBase)[0] + new_ext
        # Формирует новое имя файла, сохраняя оригинальное имя и добавляя новое расширение
        fileSaveMp4 = os.path.join(dirFilesOutput, fileBase)
        # Формирует полный путь для сохранения сконвертированного файла
        fileBase_lower = str(fileBase).lower()
        # Преобразует имя выходного файла в нижний регистр для дальнейших проверок
        
        if os.path.isfile(fileSaveMp4):
            # Проверяет, существует ли уже сконвертированный файл
            print(f"Found file: {fileSaveMp4}")
            # Выводит сообщение, если файл уже существует
            continue
            # Пропускает обработку, если файл уже существует
        str_exec = f"ffmpeg -i \"{fileName}\" -c:v copy -c:a copy \"{fileSaveMp4}\""
        # Формирует команду ffmpeg для конвертации без перекодирования
        if (".vob" in fileBase_lower) or (".mpg" in fileBase_lower):
            # Проверяет, является ли файл VOB или MPG
            str_exec = f"ffmpeg -fflags +genpts -i \"{fileName}\" -c:v copy -c:a copy \"{fileSaveMp4}\""
            # Формирует команду ffmpeg с флагом +genpts для VOB и MPG
        str_exec = f"ffmpeg -fflags +genpts -i \"{fileName}\" -c:v copy -c:a copy \"{fileSaveMp4}\""
        # Переопределяет команду ffmpeg с флагом +genpts для всех файлов
        print(f"Execute {str_exec}")  # Выводим на экран
        # Выводит сформированную команду ffmpeg
        os.system(str_exec)
        # Выполняет команду ffmpeg через систему
        fileSize = os.path.getsize(fileSaveMp4)
        # Получает размер сконвертированного файла
        if (fileSize == 0):
            # Проверяет, является ли размер файла нулевым
            os.remove(fileSaveMp4)
            # Удаляет файл, если он пустой
            fileBase = fileSplit[-1]
            # Получает имя исходного файла заново
            fileBase = os.path.splitext(fileBase)[0] + extension_map.get(os.path.splitext(fileBase)[1].lower(), ".mkv")
            # Формирует новое имя файла с новым расширением из словаря
            fileSaveMp4 = os.path.join(dirFilesOutput, fileBase)
            # Формирует новый путь для сохранения файла
            if os.path.isfile(fileSaveMp4):
                # Проверяет, существует ли уже новый файл
                print(f"Found file: {fileSaveMp4}")
                # Выводит сообщение, если файл существует
                continue
                # Пропускает обработку, если файл существует
            str_exec = f"ffmpeg -i \"{fileName}\" -c:v copy -c:a copy \"{fileSaveMp4}\""
            # Формирует новую команду ffmpeg для повторной конвертации
            print(f"Execute {str_exec}")  # Выводим на экран
            # Выводит новую команду ffmpeg
            os.system(str_exec)
            # Выполняет новую команду ffmpeg

if __name__ == "__main__":
    # Проверяет, запущен ли скрипт напрямую
    main()
    # Вызывает главную функцию main