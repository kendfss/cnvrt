cnvrt
---
  

A no frills media converter which leverages [FFMPEG]() for people who can never quite remember how its commands work.  

### Usage
```shell
> cnvrt path/one ... path/n --format mp3 --quality 92 --discard --sample
```
Will convert each argument to a 92kbps mp3 file, good for audio books or videos you hope to consume as podcasts. You can also pass directories as arguments.  
The --sample flag sends the output file to a predefined directory. This is particularly useful for people who intend to recycle media for their own creative projects.  
  
Setting this path is easy. Just run the following:  
```shell
> cnvrt --sample-dir path/to/sample/folder
```
This will save your directory to a json file which you can also edit by hand. You can get its path by:
```shell
> cnvrt --config
```
