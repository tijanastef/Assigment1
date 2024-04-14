from typing import List


class Editor(object):

    def __init__(self, editor_id:int, name:str, address:str):
        self.editor_id = editor_id
        self.name = name
        self.address = address
        self.newspaper_list: List [Newspaper] = []
        self.issue_list: List[Issue] = []


class Newspaper(object):

    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency
        self.price: float = price
        self.issues: List[Issue] = []
        self.subs: List[Subscriber]= []

    def set_editor(self, editor: Editor):
        self.editor = editor
        

class Subscriber(object):

    def __init__(self, subscriber_id: int, name: str, address:str):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.issue_recieved: List[Issue] = []
        self.subed_to: List[Newspaper] = []
        self.special_issues: List[Issue] = []
        self.missing_issues: List[Issue] = []

    def sub_to(self, newspaper):
        self.newspaper = newspaper

class Issue(object):

    def __init__(self,issue_id: int,number_of_pages:int, releasedate:str,price:float, released: bool = False):
        self.issue_id= issue_id
        self.number_of_pages = number_of_pages
        self.releasedate = releasedate
        self.price = price
        self.released: bool = released

    def set_editor(self, editor: Editor):
        self.editor = editor
