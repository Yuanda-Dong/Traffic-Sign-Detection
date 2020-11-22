## Installing RM Racer Lib 

Clone this folder.
```
git clone https://github.com/robotics-masters/rm-racer
cd rm-racer/code
```

Install
```
pip install -e .
```

Add the below to lines [manage.py](https://github.com/autorope/donkeycar/blob/dev/donkeycar/templates/complete.py#L427)
```python3
if cfg.STOP_SIGN_DETECTOR:
    #from donkeycar.parts.object_detector.stop_sign_detector import StopSignDetector
    #V.add(StopSignDetector(cfg.STOP_SIGN_MIN_SCORE, cfg.STOP_SIGN_SHOW_BOUNDING_BOX), inputs=['cam/image_array', 'pilot/throttle'], outputs=['pilot/throttle', 'cam/image_array'])
    from rmracerlib.donkey.part import RMRacerCV
    V.add(RMRacerCV(cfg), inputs=['cam/image_array', 'pilot/throttle', 'pilot/angle'], outputs=['cam/image_array', 'pilot/throttle', 'pilot/angle'], threaded=True)
```

Update myconfig.py to include these values (plus all additional for Robo HAT MM1)
```python3
STOP_SIGN_DETECTOR = True
```



## Sign detection in Simulator 

## Dependencies 

| **Python modules** |
| ------------------ |
| donkeycar          |
| gym-donkeycar      |
| opencv             |
| Tensorflow         |

Our latest simulator releases available [here](https://github.sydney.edu.au/moxu7046/COMP3988_simulator/releases)

Self-driving model (.h5 files): available in this directory 

Sign detection model (.h5 files): available in this directory 

## Instructions 

1. Change the line 18 on sign.py

   ```python
   model = keras.models.load_model('/home/yuanda/donkey/week4-
   rmracerlib/rmracerlib/sign.h5') ## change the path to the sign detection model (.h5 file), these models are included in rmracerlib
   ```

2. Change the simulator path in `myconfig.py` in `mysim` folder 

   ```python
   DONKEY_SIM_PATH = "/home/yuanda/donkey/linux_f1/my_sim_linux.x86_64" ## path to simulator 
   ```

3. Change current working directory to `mysim` folder, and run

   ```python
   python3 manage.py drive (Optional) --model models/mypilot.h5 ##slow driver for Robotics Master Challenge track
   python3 manage.py drive (Optional) --model models/pilot.h5 ##fast driver for Robotics Master Challenge track
   ```

4. If you want to drive the car manually and test purely the sign detection without the donkey
   car reacting to the sign, please uncomment line 91 in sign.py.

   

🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁
🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁🏁















