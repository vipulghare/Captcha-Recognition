import tflite_runtime.interpreter as tflite
import cv2
import numpy as np
import argparse
import os
import time


def decode(characters, y):
    y = np.argmax(np.array(y), axis=2)[:, 0]
    return ''.join([characters[x] for x in y])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--shortname', help='Shortname to put on top the results file', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)
    if args.shortname is None:
        print('Please specify the shortname')
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip() + '&'
    symbols_file.close()
    
    print("Classifying captchas with symbol set {" + captcha_symbols + "}")
    
    interpreter = tflite.Interpreter(model_path=args.model_name + '.tflite')
    interpreter.allocate_tensors()
    with open(args.output, 'w') as output_file:
        output_file.write(args.shortname + '\n')
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        count = 0
        starting_time = time.time()
        for x in sorted(os.listdir(args.captcha_dir)):
            # load image and preprocess it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            grey_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(grey_data, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            image = np.array(thresh, dtype=np.float32) / 255.0
            print(image.shape)
            (h, w) = image.shape
            image = image.reshape([-1, h, w, 1])
            # set image as input tensor
            interpreter.set_tensor(input_details[0]['index'], image)
            # interpret it
            interpreter.invoke()
            # gather predictions for each character, output goes out of place on conversion and needs sorting
            predictions = [interpreter.get_tensor(data['index']) for data in sorted(output_details, key=lambda det: det['index'])]
            output_file.write(x + "," + (decode(captcha_symbols, predictions).replace('&', '')) + "\n")
            print('Classified ' + x)
            count += 1
        print(f'Classifying {count} images took {time.time() - starting_time} seconds')

if __name__ == '__main__':
    main()
