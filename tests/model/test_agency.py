import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.newspaper import Subscriber
from ...src.model.newspaper import Editor
from ...src.model.newspaper import Issue
from ..fixtures import app, client, agency
from ...src.model.agency import Agency, Newspaper, Subscriber, Editor


def test_get_stats(agency):
    new_subscriber = Subscriber(subscriber_id=3456, name="Steve", address="Krems")
    agency.add_subscriber(new_subscriber)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    agency.subscribe_to(new_paper.paper_id, new_subscriber.subscriber_id)
    result = agency.get_stats(new_paper.paper_id)
    statistics = ({'number_of_subscribers':1,'monthly_revenue':3.14, 'annual_revenue':37.68})
    assert result == statistics

def test_subscriber_stats(agency):
    new_subscriber = Subscriber(subscriber_id=44, name="Steve", address="Krems")
    agency.add_subscriber(new_subscriber)
    new_paper = Newspaper(paper_id=9,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    agency.subscribe_to(new_paper.paper_id, new_subscriber.subscriber_id)
    result = agency.subscriber_stats(new_subscriber.subscriber_id)
    assert result == (3.14, 37.68, {})

def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1

    
def test_get_newspaper(agency):
    new_paper = Newspaper(paper_id=4399,
                        name="Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    paper = agency.get_newspaper(new_paper.paper_id)
    assert new_paper == paper


def test_issue_info(agency):
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    assert new_issue == issue

def test_get_editor(agency):
    e1 = Editor(editor_id=1, name="Editor 1", address="Beograd")
    agency.add_editor(e1)
    editor = agency.get_editor(e1.editor_id)
    assert e1 == editor

def test_all_editors(agency):
    before = len(agency.editors)
    e1 = Editor(editor_id=1, name="Editor 1", address="Beograd")
    e2 = Editor(editor_id=1, name="Editor 2", address="Krems")
    agency.add_editor(e1)
    agency.add_editor(e2)
    after = len(agency.all_editors())
    assert after == before +2

def test_missing_issues(agency):
    new_subscriber = Subscriber(subscriber_id=4, name="Subscriber", address="Vienna")
    agency.add_subscriber(new_subscriber)
    sub = agency.get_subscriber(new_subscriber.subscriber_id)

    before = len(agency.missing_issues(sub.subscriber_id))

    new_paper = Newspaper(paper_id=456,
                        name="Comics",
                        frequency=5,
                        price=6.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=6, number_of_pages=23, releasedate='25.3.2024', released=False, price=34)
    agency.add_issue(new_issue, new_paper.paper_id)


    agency.subscribe_to_special_issue(new_paper.paper_id, sub.subscriber_id, new_issue.issue_id)
    agency.release_issue(new_issue.issue_id, new_paper.paper_id)
    
    after = len(agency.missing_issues(sub.subscriber_id))
    assert after == before +1

def test_get_subscriber(agency):
    s1 = Subscriber(subscriber_id=1, name="Subscriber 1", address="Beograd")
    agency.add_subscriber(s1)
    subscriber = agency.get_subscriber(s1.subscriber_id)
    assert s1 == subscriber


def test_all_newspaper(agency):
    before = len(agency.all_newspapers())
    paper1 = Newspaper(123,"B92",45,67 )
    paper2 = Newspaper(344,"Kurir", 62, 54.3)
    agency.add_newspaper(paper1.paper_id)
    agency.add_newspaper(paper2.paper_id)
    assert len(agency.all_newspapers()) == before +2

def test_add_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber = Subscriber(subscriber_id=1, name="Test", address="512 Main Rt")
    agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before +1

def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=1, name="Editor 3", address="Adresa")
    agency.add_editor(new_editor)
    assert len(agency.all_editors())==before + 1

def test_get_editor_issues(agency):
    editor = Editor(editor_id=1, name="Editor", address="Krems")
    agency.add_editor(editor)
    before = len(editor.issue_list)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    after = len(agency.set_editor1(issue.issue_id, paper.paper_id, editor.editor_id))

    assert after == before +1

def test_set_editor1(agency):
    editor = Editor(editor_id=1, name="Editor", address="Krems")
    agency.add_editor(editor)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    agency.set_editor1(issue.issue_id, paper.paper_id, editor.editor_id )
    issue_editor = issue.editor
    assert issue_editor.editor_id == editor.editor_id

def test_set_editor2(agency):
    editor = Editor(editor_id=1, name="Editor", address="Krems")
    agency.add_editor(editor)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    paper = agency.get_newspaper(new_paper.paper_id)
    agency.set_editor2(paper.paper_id, editor.editor_id )
    paper_editor =paper.editor 
    assert paper_editor.editor_id == editor.editor_id

def test_all_subscribers(agency):
    before = len(agency.all_subscribers())
    s1 = Subscriber(subscriber_id=23, name="Subscriber 1", address="Beograd")
    s2 = Subscriber(subscriber_id=15, name="Subscriber 2", address="Krems")
    agency.add_subscriber(s1.subscriber_id)
    agency.add_subscriber(s2.subscriber_id)
    assert len(agency.all_subscribers()) == before +2

def test_delete_newspaper(agency):
    new_paper = Newspaper(paper_id=381,
                        name="Blic",
                        frequency=1,
                        price=32.14)
    agency.add_newspaper(new_paper)
    before = len(agency.all_newspapers())
    agency.remove_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before-1


def test_remove_editor(agency):
    new_editor = Editor(editor_id=1, name="Tijana", address="Krems")
    agency.add_editor(new_editor)
    before = len(agency.all_editors())
    agency.remove_editor(new_editor)
    assert len(agency.all_editors()) == before-1

def test_remove_subscriber(agency):
    new_subscriber = Subscriber(subscriber_id=1, name="Matija", address="Jagodina")
    agency.add_subscriber(new_subscriber)
    before = len(agency.all_subscribers())
    agency.remove_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before-1

def test_remove_issue(agency):
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    before = len(paper.issues)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    agency.remove_issue(issue.issue_id, paper.paper_id)
    assert len(paper.issues) == before - 1

def test_add_issue(agency):
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    before = len(paper.issues)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    agency.add_issue(issue.issue_id, paper.paper_id)
    assert len(paper.issues) == before + 1

def test_subscribe_to_newspaper(agency):
    new_subscriber = Subscriber(subscriber_id=1, name="Editor 1", address="Krems")
    agency.add_subscriber(new_subscriber)
    before = len(new_subscriber.subed_to)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    agency.subscribe_to(new_paper.paper_id, new_subscriber.subscriber_id)
    sub = agency.get_subscriber(new_subscriber.subscriber_id)
    assert len(sub.subed_to) == before + 1

def test_subscribe_to_special_issue(agency):
    new_subscriber = Subscriber(subscriber_id=1, name="Editor 1", address="Krems")
    agency.add_subscriber(new_subscriber)
    before = len(new_subscriber.special_issues)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=0)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    sub = agency.get_subscriber(new_subscriber.subscriber_id)
    agency.subscribe_to_special_issue(paper.paper_id, sub.subscriber_id, issue.issue_id)
    assert len(sub.subed_to) == before + 1


def test_list_all_issues_of_newspaper(agency):
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    before = len(paper.issues)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    agency.add_issue(issue.issue_id, paper.paper_id)
    after = len(agency.all_issues(paper.paper_id))
    assert after == before + 1


def test_release_issue(agency):
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    agency.add_issue(issue.issue_id, paper.paper_id)
    before = issue.released
    agency.release_issue(issue.issue_id, paper.paper_id)
    after = issue.released
    assert before != after

def test_deliver_issue(agency):
    new_subscriber = Subscriber(subscriber_id=1, name="Editor 1", address="Krems")
    agency.add_subscriber(new_subscriber)
    before = len(new_subscriber.issue_recieved)
    new_paper = Newspaper(paper_id=999,
                        name="Simpsons Comic",
                        frequency=7,
                        price=3.14)
    agency.add_newspaper(new_paper)
    new_issue = Issue(issue_id=46, number_of_pages=123, releasedate='20.3.2024', released=False, price=234)
    agency.add_issue(new_issue, new_paper.paper_id)
    paper = agency.get_newspaper(new_paper.paper_id)
    issue = agency.issue_info(new_issue.issue_id, new_paper.paper_id)
    sub = agency.get_subscriber(new_subscriber.subscriber_id)
    agency.subscribe_to_special_issue(paper.paper_id, sub.subscriber_id, issue.issue_id)
    after = len(agency.deliver(paper.paper_id, issue.issue_id, sub.subscriber_id))
    assert after == before + 1
  