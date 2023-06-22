import tensorflow as tf


def foodnotfood(image_path):
    model_path = "foodnotfoodmode.tflite"
    image_path = image_path
    img_shape = 224

    # Read in the image
    img = tf.io.read_file(image_path)
    # Decode it into a tensor
    img = tf.image.decode_jpeg(img)
    # Resize the image
    img = tf.image.resize(img, [img_shape, img_shape])

    # Turn img to uint8 (for TFLite)
    img = tf.cast(img, dtype=tf.uint8)

    # Expand dimensions for batch size
    img = tf.expand_dims(img, axis=0)

    # Loading model
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]

    # Prediction
    interpreter.set_tensor(input_index, img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)
    class_names = {0: "food", 1: "not_food"}
    result = class_names[output.argmax()]
    return result
