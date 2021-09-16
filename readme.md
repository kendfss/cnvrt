cnvrt
---
  

A low fuss media converter which leverages [FFMPEG](https://ffmpeg.org/) for people who can never quite remember how its commands work.  

### Usage
```shell
> cnvrt path/one ... path/n --format mp3 --quality 92 --discard --sample
> cnvrt path/one ... path/n -fmp3 --dsq92
```
Either of the above will convert each argument to a 92kbps mp3 file; good for audio books or videos you hope to consume as podcasts. You can also pass directories as arguments.  
You can also ignore any paths that aren't to audio files by using the `-a` or `--audio` switches.
The --sample flag sends the output file to a predefined directory. This is particularly useful for people who intend to recycle media for their own creative projects.  
Setting this path is automated, just follow the prompt after using the `-s` or `--sample` flag.
- This will save your directory to a json file which you can also edit by hand. You can get its path by:
    ```shell
    > cnvrt --config # or -c
    ```


### todo
- image processing is not supported
- could probably afford to consolidate the parts into objects
