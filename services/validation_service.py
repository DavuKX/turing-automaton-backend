import json

from dto.validated_word import ValidatedWordCreate
from repositories.validated_words_repository import ValidatedWordsRepository


class ValidationService:
    def __init__(self, automaton_data: dict, word: str, uuid: str):
        self.automaton_data = automaton_data
        self.word = word
        self.uuid = uuid

    def validate(self):
        current_state = self.automaton_data['initialState']
        acceptance_states = self.automaton_data['acceptanceStates']
        tape = list(self.word)
        current_symbol_index = 0
        path = []

        for symbol in tape:
            possible_transitions = self.automaton_data['transitions'][current_state]
            possible_transitions = [transition for transition in possible_transitions if
                                    transition['read'] == symbol or transition['read'] == '']

            transition = possible_transitions[0]

            read = transition['read'] if transition['read'] != '' else 'λ'
            write = transition['write'] if transition['write'] != '' else 'λ'
            action = transition['move']
            path.append({
                'initial_state': current_state,
                'next_state': transition['to'],
                'tape': tape.copy(),
                'current_symbol_index': current_symbol_index,
                'edge_label': read + '/' + write + '/' + action,
                'symbol': symbol,
            })

            tape[current_symbol_index] = transition['write']
            current_state = transition['to']

            if action == 'R':
                current_symbol_index += 1
            elif action == 'L':
                current_symbol_index -= 1

        transition = self.automaton_data['transitions'][current_state]
        transition = [transition for transition in transition if transition['read'] == '']
        transition = transition[0]
        current_symbol_index -= 1

        path.append({
            'initial_state': current_state,
            'next_state': transition['to'],
            'tape': tape.copy(),
            'current_symbol_index': current_symbol_index,
            'edge_label': 'λ/λ/' + transition['move'],
            'symbol': 'λ',
        })
        current_state = transition['to']

        while current_symbol_index > 0:
            transition = self.automaton_data['transitions']['q2']
            transition = [transition for transition in transition if transition['read'] == 'a']
            transition = transition[0]
            current_symbol_index -= 1
            path.append({
                'initial_state': current_state,
                'next_state': transition['to'],
                'tape': tape.copy(),
                'current_symbol_index': current_symbol_index,
                'edge_label': 'a/a/' + transition['move'],
                'symbol': 'a',
            })
            current_state = transition['to']

        path.append({
            'initial_state': current_state,
            'next_state': 'q3',
            'tape': tape.copy(),
            'current_symbol_index': current_symbol_index,
            'edge_label': 'λ/λ/R',
            'symbol': 'λ',
        })

        is_valid = current_state in acceptance_states
        return self.save_result(is_valid, tape, path)

    def save_result(self, is_valid: bool, tape: list, path: list):
        repository = ValidatedWordsRepository()
        db_validated_word = ValidatedWordCreate(
            uuid=self.uuid,
            word=self.word,
            result_word=''.join(tape),
            is_valid=is_valid,
            path=json.dumps(path)
        )
        return repository.create(db_validated_word)
