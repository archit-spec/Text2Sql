# Reencode, trim, and set frame rate to 30 fps
ffmpeg -i /home/dumball/alo.mp4 -t 10 -r 30 -c:v libx264 -c:a aac -strict experimental -b:a 192k -movflags faststart reencoded1.mp4
ffmpeg -i /home/dumball/accha.mp4 -t 10 -r 30 -c:v libx264 -c:a aac -strict experimental -b:a 192k -movflags faststart reencoded2.mp4

# Get dimensions of the first video
WIDTH1=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 reencoded1.mp4)
HEIGHT1=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 reencoded1.mp4)

# Get dimensions of the second video
WIDTH2=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 reencoded2.mp4)
HEIGHT2=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 reencoded2.mp4)

# Calculate maximum width and height
MAX_WIDTH=$(($WIDTH1 > $WIDTH2 ? $WIDTH1 : $WIDTH2))
MAX_HEIGHT=$(($HEIGHT1 > $HEIGHT2 ? $HEIGHT1 : $HEIGHT2))

# Pad the videos to the maximum dimensions
ffmpeg -i reencoded1.mp4 -vf "scale=$MAX_WIDTH:$MAX_HEIGHT:force_original_aspect_ratio=decrease,pad=$MAX_WIDTH:$MAX_HEIGHT:(ow-iw)/2:(oh-ih)/2:color=white" padded1.mp4
ffmpeg -i reencoded2.mp4 -vf "scale=$MAX_WIDTH:$MAX_HEIGHT:force_original_aspect_ratio=decrease,pad=$MAX_WIDTH:$MAX_HEIGHT:(ow-iw)/2:(oh-ih)/2:color=white" padded2.mp4

# Combine the videos vertically
ffmpeg -i padded1.mp4 -i padded2.mp4 -filter_complex "vstack=inputs=2" combined.mp4

