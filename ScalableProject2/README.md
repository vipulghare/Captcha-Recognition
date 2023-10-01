# ScalableProject2
Tensorflow based captcha recognition

## Running the code

Below are detailed explanation on how to run each piece of code, with example commands showing the parameters we used to achieve our results. Generate.py, train.py, and convert.py should be ran on a high powered machine, preferably with a strong GPU to speed up the training, while classify_lite.py and get_data.py are to be ran on the Raspberry pi.

## Dependencies

In order to successfully run the code for generating data, training and converting the model, a number of dependencies must be installed using `python3 -m pip install {name_of_dependency}`

### For the training machine
- numpy
- opencv-python
- captcha
- tensorflow

### For the Raspberry pi
- requests
- numpy
- opencv-python
- tflite-runtime

### Generate.py
Generates random captchas to be used as training or validation datasets.

To run, use `python3 generate.py --width 128 --height 64 --lower-length 1 --upper-length 6 --count 128000 --output-dir training_set --symbols symbols.txt 
--dict-name training_dict.txt`

### train.py
Trains the model to recognise captchas based on the training and validation datasets.

To run, use `python3 train.py --width 128 --height 64 --length 6 --batch-size 64 --epochs 5 --output-model-name model --symbols symbols.txt  
--train-dataset training_set --train-dict training_dict.txt --validate-dataset validation_set --validate-dict validate_dict.txt`

### convert.py
Converts a regular tensorflow model to tflite format which can run on Raspberry PIs

To run, use `python3 convert.py --model-name model --output converted_model`

### get_data.py
Downloads the captcha images for the given user.

To run use `no_proxy="" python3 get_data.py --shortname ogoreka`

### classify_lite.py
Runs the model to classify images using tensorflow lite. Pass in the name to the model converted with convert.py

To run, use `python3 classify_lite.py --model-name model --captcha-dir captchas --output output.txt --symbols symbols.txt --shortname ogoreka`
