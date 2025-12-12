import bardapi
import os


os.environ['_BARD_API_KEY'] = ''


def call(prompt):
    print('prompt: ', prompt)
    response = bardapi.core.Bard().get_answer(prompt)
    for i, choice in enumerate(response['choices']):
        print(choice['content'][0], '\n')

    return response
