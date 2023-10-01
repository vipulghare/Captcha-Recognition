import tensorflow as tf
import tensorflow.lite as tflite
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to convert', type=str)
    parser.add_argument('--output', help='Name under which the converted model should be saved', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to convert")
        exit(1)

    if args.output is None:
        print("Please specify the output model name")
        exit(1)

    json_file = open(args.model_name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = tf.keras.models.model_from_json(loaded_model_json)
    model.load_weights(args.model_name + '.h5')
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    converted_model = converter.convert()

    with open(args.output + '.tflite', 'wb') as f:
        f.write(converted_model)


if __name__ == '__main__':
    main()
