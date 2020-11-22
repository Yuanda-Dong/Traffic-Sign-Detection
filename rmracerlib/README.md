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
