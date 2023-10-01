#!/usr/bin/env python3

import os
import numpy
import random
import string
import json
import cv2
import argparse
import captcha.image
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', help='Width of captcha image', type=int)
    parser.add_argument('--height', help='Height of captcha image', type=int)
    parser.add_argument('--upper-length', help='Upper length limit of captchas in characters', type=int)
    parser.add_argument('--lower-length', help='Lower length limit of captchas in characters', type=int)
    parser.add_argument('--count', help='How many captchas to generate', type=int)
    parser.add_argument('--output-dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--dict-name', help = 'name for the dictionary file, translating captcha ids into symbols', type=str)
    args = parser.parse_args()

    if args.width is None:
        print("Please specify the captcha image width")
        exit(1)

    if args.height is None:
        print("Please specify the captcha image height")
        exit(1)

    if args.upper_length is None:
        print("Please specify the captcha length")
        exit(1)

    if args.lower_length is None:
        print("Please specify the captcha length")
        exit(1)

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)
    start_time = time.time()
    captcha_generator = captcha.image.ImageCaptcha(width=args.width, height=args.height)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Generating captchas with symbol set {" + captcha_symbols + "}")

    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)
    dict = {}
    for i in range(args.count):
        random_str = ''.join([random.choice(captcha_symbols) for j in range(random.randint(args.lower_length, args.upper_length))])
        image_path = os.path.join(args.output_dir, str(i) + '.png')
        dict[i] = random_str
        image = numpy.array(captcha_generator.generate_image(random_str))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # get threshold image
        ret, thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite(image_path, thresh_img)
    with open(args.dict_name, 'w') as dict_file:
        for index in dict:
            dict_file.write(str(index) + ' ' + dict[index] + '\n')
    print(f"Generating {args.count} captchas took {time.time()-start_time} seconds.")

if __name__ == '__main__':
    main()
