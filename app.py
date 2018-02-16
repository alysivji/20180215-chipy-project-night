from __future__ import unicode_literals
import statistics

from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
import meetup.api


def get_names():
    client = meetup.api.Client('3f6d3275d3b6314e73453c4aa27')

    rsvps = client.GetRsvps(event_id='239174106', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    names = []
    for member in members.results:
        try:
            names.append(member['name'])
        except:
            pass # ignore those who do not have a complete profile

    return names


command_completer = WordCompleter(['add'], ignore_case=True)


def execute(command, person_num_line):
    # parse command
    # add <name> <lines>
    command = command.strip()
    parsed_command = command.split(' ')
    entered_command = parsed_command.pop(0)

    if entered_command == 'add':
        num_lines_of_code = parsed_command.pop(-1)
        parsed_name = ' '.join(parsed_command)

        try:
            int_num_lines_of_code = int(num_lines_of_code)
            person_num_line[parsed_name] = int_num_lines_of_code
        except ValueError:
            return "Please enter a number"

        return f'{parsed_name} wrote {num_lines_of_code} of code'
    elif entered_command == 'list':
        basket = []
        for p, n in person_num_line.items():
            basket.append('{0}, {1}'.format(p, n))
        median_num_lines = statistics.median(person_num_line.values())
        num_people = len(person_num_line.keys())
        people_and_lines = '\n'.join(basket)
        return '{0} \n Num of people: {1} \n Median line count {2}'.format(
            people_and_lines,
            str(num_people),
            str(median_num_lines)
        )
    elif entered_command == 'team':
        return 'We did not finish this'

    return 'Please enter a real command'


def main():
    history = InMemoryHistory()
    person_num_line = {}

    while True:
        try:
            text = prompt('> ',
                          completer=command_completer,
                          history=history,
                          on_abort=AbortAction.RETRY)
            messages = execute(text, person_num_line)

            print(messages)
        except EOFError:
            break  # Control-D pressed.

    print('GoodBye!')


if __name__ == '__main__':
    main()
