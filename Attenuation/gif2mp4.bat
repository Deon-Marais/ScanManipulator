"D:\bin\ffmpeg-3.4.2-win64-static\bin\ffmpeg.exe" -y -i %1 -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" %1.mp4

"D:\bin\ffmpeg-3.4.2-win64-static\bin\ffmpeg.exe" -y -i %1 %1.avi