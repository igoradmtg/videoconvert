import os
# Разделить файлы на куски размером 1800 Мб

# Windows
#dirName = r"z:\001\VideoBig"
#dirNameOut = r"z:\001\Out"

# Ubuntu
dirName = r"/usr/www/upl2"
dirNameOut = r"/usr/www/upl3"
fileSize = "size:500M"
fileSize = "duration:00:05:00.000"
def main():
    files = []
    for r, d, f in os.walk(dirName):
        for file in f:
            if ('.mp4' in file) or ('.mpg' in file) or ('.avi' in file) or ('.wmv' in file) or ('.mkv' in file):
                file_name, file_extension = os.path.splitext(file)
                files.append({'oldName':os.path.join(r,file),'newName':os.path.join(dirNameOut,file)})
    print(files)
    for fileName in files:
        print(fileName)
        oldName = fileName['oldName']
        newName = fileName['newName']
        strExec = f'mkvmerge --split {fileSize} -o "{newName}" "{oldName}"'
        print(strExec)
        os.system(strExec)

if __name__ == '__main__':
    main()
