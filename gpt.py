import os
import openai
from clarifaicheck import *

os.environ["http_proxy"] = "127.0.0.1:7890"  # you may need to change this according to ya proxy
os.environ["https_proxy"] = "127.0.0.1:7890"  # same with this


def gpt(check, personalities, image_path, openai_key, clarifai_key):
    openai.api_key = openai_key
    if check == "not_food":
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are speaking like {personalities}."},
                    {"role": "user", "content": "I just sent you a picture that is not a food. Come up with a playful "
                                                "jab that what I sent you isn't a food and I should do better"}
                ]
            )

            return completion.choices[0].message.content, "true"
        except Exception as e:
            return e, "openai"
    else:
        food = clarifai(image_path, clarifai_key)

        if food == "None":
            return "Error: Wrong Clarifai key", "clarifai"
        else:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are speaking like {personalities}. "
                                                      f"Guess the food based of the user input then speak on it. Be "
                                                      f"like I guess I'm seeing is blabla based on your input and then "
                                                      f"give more what details with about a hundred words"},
                        {"role": "user", "content": food}
                    ]
                )

                completion2 = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are speaking like {personalities}. "
                                                      f"Give alternatives to the food in a list format, beginning "
                                                      f"with here are some"},
                        {"role": "user", "content": food}
                    ]
                )

                return completion.choices[0].message.content, completion2.choices[0].message.content
            except Exception as e:
                return e, "openai"
