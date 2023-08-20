set /p 82103=<82103.txt
call C:\Users\82103\anaconda3\Scripts\activate.bat C:\Users\82103\anaconda3\envs\wav2lip

python inference.py --checkpoint_path %1 --face %2 --audio %3 --pads %~4 --resize_factor %5 %~6

call conda deactivate