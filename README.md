# facedtc
Face detection and cropping for model training

---

*face_extract.py* : That script will read all images provided in the "inputs" directory, will scan faces and then select an area around the face, crop it and then resize to 512x512 so that it can be use to train a stable diffusion model (Using Dreambooth, textual inversion, Lora or hypernetwork)
It doesn't take any parameter and erase the content of "outputs" at each start
```batch
python face_extract.py
```
---

*frames_extractor.py* : You specify an interval and a video file and it will extract all frames contained between the start and stop parameters. Additionaly you can enable a feature that will discard any frames that doesn't contain a face. 
Only extracting frames example :
```batch
python .\frames_extractor.py  --start 40:00 --stop 41:42  --directory "frames"  --interval 0.5 movie.mkv
```
That will extract a frame every 0.5s starting from 40:00 minutes in the film to 41:42. Meaning it will extract 84 frames.

Using the face detection feature : 
```batch
python .\frames_extractor.py  --start 1:00:00 --stop 1:08:00  --directory "frames-faces" --face-only --face-size 150 --detection-quality 5 --interval 1 movie.mkv
```
That will extract a frame every second from 1hour in the movie to 1h08 but will discard them if there is no face detected in it. face-size specify the minimum face size in pixels and detection quality will impact the detection tolerance, higher will yield less result but of better quality.

---

*prompt_helper_guy.py* : It will open a GUI window and will ask you to choose a directory. It will let you create a txt file for each pictures in that directory. The idea is to write the prompts press enter and then load the next pictures. The previous prompt is stored in the clipboard for faster typing.