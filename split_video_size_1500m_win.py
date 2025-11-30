import os
# Разделить файлы на куски размером 333 Мб

# Windows
dirName = r"W:\001\VideoBig"
dirNameOut = r"W:\001\VideoSmall"

# Ubuntu
#dirName = r"/usr/www/upl2"
#dirNameOut = r"/usr/www/upl3"
fileSize = "size:1500M"
def main():
    files = []
    for r, d, f in os.walk(dirName):
        for file in f:
            if ('.mp4' in file) or ('.mpg' in file) or ('.avi' in file) or ('.wmv' in file) or ('.mkv' in file) or ('.m4v' in file):
                file_name, file_extension = os.path.splitext(file)
                files.append({'oldName':os.path.join(r,file),'newName':os.path.join(dirNameOut,file)})
    #print(files)
    for fileName in files:
        #print(fileName)
        oldName = fileName['oldName']
        newName = fileName['newName']
        strExec = f'mkvmerge --split {fileSize} -o "{newName}" "{oldName}"'
        print(strExec)
        os.system(strExec)

if __name__ == '__main__':
    main()
