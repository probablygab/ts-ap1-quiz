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

# 10 new tests
def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_question_with_invalid_max_selections():
    q = Question(title='q1', max_selections=0)

    with pytest.raises(Exception):
        q.select_choices([1])

def test_create_full_custom_question():
    question = Question(title='q1', points=50, max_selections=3)
    assert question.title == 'q1'
    assert question.points == 50
    assert question.max_selections == 3

def test_correct_choices():
    question = Question(title='q1', points=50, max_selections=3)
    question.add_choice('a', True)
    question.add_choice('b', False)
    question.add_choice('c', True)

    correct_choices = question.select_choices([1, 2, 3])
    assert correct_choices == [1, 3]

def test_remove_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    question.remove_choice_by_id(1)
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    question.remove_all_choices()
    assert len(question.choices) == 0

def test_remove_choice_by_id_not_found():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    with pytest.raises(Exception):
        question.remove_choice_by_id(3)

def test_remove_choice_by_id_success():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)

    question.remove_choice_by_id(2)
    assert len(question.choices) == 1
    assert question.choices[0].text == 'a'

def test_set_correct_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)

    question.set_correct_choices([1, 2])
    assert question.choices[0].is_correct == True
    assert question.choices[1].is_correct == True
    assert question.choices[2].is_correct == False

def test_set_correct_choices_invalid():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)

    with pytest.raises(Exception):
        question.set_correct_choices([4])

# 2 new tests with fixtures
@pytest.fixture
def template_question():
    q = Question(title='Template Question', points=10, max_selections=3)
    
    q.add_choice('A', False)
    q.add_choice('B', False)
    q.add_choice('C', True)

    return q

def test_select_correct_choices_fixture(template_question):
    selected_choices = template_question.select_choices([1, 3])
    assert selected_choices == [3]

def test_remove_choice_by_id_fixture(template_question):
    template_question.remove_choice_by_id(2)
    assert len(template_question.choices) == 2
    assert template_question.choices[0].text == 'A'
    assert template_question.choices[1].text == 'C'