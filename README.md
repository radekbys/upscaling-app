# upscaling-app

a simple app using my upscalers, it is basically just a prototype, but I am fine with it at this stage

# weights for the models

app uses model weights which cannot be uploaded to github, too large files
link to the compressed folder - https://drive.google.com/file/d/16fph_2JdVmQ8kbixpkaQVGPi1OKDbIfv/view?usp=sharing

# running the application

You dont need to download these files, just use docker:

docker-compose build

docker-compose up

# to run on a machine without nvidia gpu comment out last line of docker-compose.yml

tested on a laptop with no nvidia gpu, wont upscale images larger than around 720p (HD), will get a timeout after 120seconds
5070ti can upscale even 4k into 8k easily within that timeframe
