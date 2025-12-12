import bardapi
import os

# os.environ['_BARD_API_KEY'] = 'XQhe5-0j5-0oh-b8SPqu8WUd39PtI0VERWfPWQN6f8-gtEdkWg2kDfHUz0p-rsDgkzN_tw.'
os.environ['_BARD_API_KEY'] = 'Ywhe52ZAS1X07XH77klo3Tbi41e4bWebbo4v9Tlmzgeg7gMblVdRhdMkNV7ItwYmcgxhww.'


def call(prompt):
    print('prompt: ', prompt)
    response = bardapi.core.Bard().get_answer(prompt)
    for i, choice in enumerate(response['choices']):
        print(choice['content'][0], '\n')

    return response
