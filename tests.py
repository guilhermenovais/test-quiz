import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)


def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)


def test_add_choice_returns_choice_with_sequential_id():
    question = Question(title='q1')
    first_choice = question.add_choice('a')
    second_choice = question.add_choice('b')

    assert first_choice.id == 1
    assert second_choice.id == 2


def test_remove_choice_by_id_removes_only_target_choice():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')

    question.remove_choice_by_id(c1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == c2.id


def test_remove_choice_by_id_with_invalid_id_raises_exception_and_preserves_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    with pytest.raises(Exception):
        question.remove_choice_by_id(99)

    assert len(question.choices) == 2


def test_remove_all_choices_clears_question_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices_marks_multiple_choices_as_correct():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')

    question.set_correct_choices([c1.id, c3.id])

    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct
    assert question.choices[2].is_correct
    assert c2.id == 2


def test_set_correct_choices_with_invalid_choice_id_raises_exception():
    question = Question(title='q1')
    c1 = question.add_choice('a')

    with pytest.raises(Exception):
        question.set_correct_choices([c1.id, 99])


def test_correct_selected_choices_returns_only_selected_correct_ids():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    question.set_correct_choices([c1.id, c3.id])

    result = question.correct_selected_choices([c1.id, c2.id])

    assert result == [c1.id]


def test_correct_selected_choices_exceeding_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')

    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])
