OLD_IFS=$IFS

IFS=$'\n'
for i in $( ls *.mp3 );
	do echo ffmpeg -i \""$i"\" "${i%.*}.wav";
done
echo 'wodim -v -fix -eject dev='/dev/sr0' -audio -pad *.wav'
IFS=$OLD_IFS
