from collections import OrderedDict

import click

from changes.commands import note, error


def choose_labels(alternatives):
    """
    Prompt the user select several labels from the provided alternatives.

    At least one label must be selected.

    :param list alternatives: Sequence of options that are available to select from
    :return: Several selected labels
    """
    if not alternatives:
        raise ValueError

    if not isinstance(alternatives, list):
        raise TypeError

    choice_map = OrderedDict(
      ('{}'.format(i), value) for i, value in enumerate(alternatives, 1)
    )
    # prepend a termination option
    input_terminator = '0'
    choice_map.update({input_terminator: '<done>'})
    choice_map.move_to_end('0', last=False)

    choice_indexes = choice_map.keys()

    choice_lines = ['{} - {}'.format(*c) for c in choice_map.items()]
    prompt = '\n'.join((
        'Select labels:',
        '\n'.join(choice_lines),
        'Choose from {}'.format(', '.join(choice_indexes))
    ))

    user_choices = set()
    user_choice = None

    while not user_choice == input_terminator:
        if user_choices:
            note('Selected labels: [{}]'.format(', '.join(user_choices)))

        user_choice = click.prompt(
            prompt,
            type=click.Choice(choice_indexes),
            default=input_terminator,
        )
        done = user_choice == input_terminator
        new_selection = user_choice not in user_choices
        nothing_selected = not user_choices

        if not done and new_selection:
            user_choices.add(choice_map[user_choice])

        if done and nothing_selected:
            error('Please select at least one label')
            user_choice = None

    return user_choices
