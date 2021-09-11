import os, subprocess, argparse, json


this = __file__
here = os.path.dirname(__file__)
settings_file_path = os.path.join(here, "settings.json")

def load_settings(path:str) -> dict[str|str]:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return dict()

def save_settings(path:str, data:dict):
    with open(path, "w") as f:
        json.dump(data, f, indent=2*" ", sort_keys=True)

settings = load_settings(settings_file_path)
sample_folder = settings.get("sample_folder")

def convert(file, format='.mp3', quality=320) -> str:
    format = "."+format if format[0]!='.' else format
    name = file.split(os.sep)[-1].split('.')[0]
    folder = os.sep.join(file.split(os.sep)[:-1])
    new = os.path.join(folder, name + format)
    cmd = ["ffmpeg", "-y", "-i", file, "-ab", str(quality * 1000), new]
    subprocess.run(cmd)
    return new

def path(argument:str) -> str:
    if os.path.exists(argument):
        return os.path.abspath(argument)
    raise FileNotFoundError(f'Couldn\'t find "{argument}" in the file system')

def get_sample_dir():
    pth = settings.get("sample_folder")
    while None==pth:
        pth = input("\nWhere do you want to keep your samples? (tree will be generated automatically):\n\t")
    pth = path(pth)
    os.makedirs(pth, exist_ok=True)
    return pth

def handle(args:argparse.Namespace, original:str, product:str):
    if args.sample:
        settings["sample_folder"] = sample_folder = get_sample_dir()
        save_settings(settings_file_path, settings)

        _, name = os.path.split(product)
        os.rename(product, os.path.join(sample_folder, name))
    
    if args.discard:
        os.remove(original)

def main():
    parser = argparse.ArgumentParser(description="Convert files with ffmpeg")
    parser.add_argument("path", type=path, nargs="+", help="path to the file(s) you wish to convert")
    parser.add_argument("-f", "--format", default="ogg", type=str, help="new format for the file(s) [default=ogg]")
    parser.add_argument("-q", "--quality", default=450, type=int, help="quality (in kbps) of the output file(s) [default=450]")
    parser.add_argument("-d", "--discard", default=False, action="store_true", help="Switch to delete file after conversion is complete")
    parser.add_argument("-s", "--sample", default=False, action="store_true", help="Add file to sample library")
    parser.add_argument("-c", "--config", default=False, action="store_true", help="Print path to settings file")
    
    args = parser.parse_args()
    
    if args.config:
        print(settings_file_path)
    for p in args.path:
        if os.path.isdir(p):
            for name in os.listdir(p):
                src = os.path.join(p, name)
                out = convert(src, format=args.format, quality=args.quality)
                handle(args=args, original=src, product=out)
        else:
            out = convert(p, format=args.format, quality=args.quality)
            handle(args=args, original=p, product=out)

if __name__ == '__main__':
    main()
