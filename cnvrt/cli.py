import os, subprocess, argparse


def convert(file, format='.mp3', quality=320):
    format = "."+format if format[0]!='.' else format
    name = file.split(os.sep)[-1].split('.')[0]
    folder = os.sep.join(file.split(os.sep)[:-1])
    new = os.path.join(folder, name + format)
    cmd = f'ffmpeg -y -i "{file}" -ab  {quality*1000} "{new}"' if quality != 0 else f'ffmpeg -y -i "{file}"'
    subprocess.run(cmd)
    

def path(argument):
    if os.path.exists(argument):
        return os.path.abspath(argument)
    raise FileNotFoundError(f'Couldn\'t find "{argument}" in the file system')

def main():
    parser = argparse.ArgumentParser(description="Convert files with ffmpeg")
    parser.add_argument("path", type=path, nargs="+", help="path to the file(s) you wish to convert")
    parser.add_argument("--format", default="mp3", type=str, help="new format for the file(s)")
    parser.add_argument("--quality", default=450, type=int, help="quality (in kbps) of the output file(s)")
    
    args = parser.parse_args()
    
    for p in args.path:
        if os.path.isdir(p):
            for name in os.listdir(p):
                convert(os.path.join(p, name), format=args.format, quality=args.quality)
        else:
            convert(p, format=args.format, quality=args.quality)

if __name__ == '__main__':
    main()
