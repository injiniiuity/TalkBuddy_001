set /p 82103=<82103.txt
call C:\Users\82103\anaconda3\Scripts\activate.bat C:\Users\82103\anaconda3\envs\wav2lip-ui
python inference.py --checkpoint_path checkpoints/wav2lip.pth --face input/pic.png --audio input/output.wav
python ui.py


call conda deactivate