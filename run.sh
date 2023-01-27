rm -f ./input/audio.mp3
rm -f ./input/fps.json
rm -f ./images/*.png
rm -f ./output/output.avi
rm -f ./output/final.mp4

python main.py $1 extract
go run parallel.go
python main.py $1 write

rm -f ./input/audio.mp3
rm -f ./input/fps.json
rm -f ./images/*.png
rm -f ./output/output.avi
