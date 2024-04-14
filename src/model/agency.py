from typing import List, Optional

from .newspaper import Newspaper

from .newspaper import Editor

from .newspaper import Subscriber

from .newspaper import Issue


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        self.newspapers.append(new_paper)
        return new_paper

    def get_newspaper(self, paper_id: int) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, issue: Newspaper):
        for element in issue.issues:
            self.remove_issue(element.issue_id,issue.paper_id)
        self.newspapers.remove(issue)

    def add_editor(self, new_editor: Editor):
        self.editors.append(new_editor)

    def get_editor(self, editor_id:int) -> Optional[Editor]:
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None

    def all_editors(self) -> List[Editor]:
        return self.editors

    def remove_editor(self, editor: Editor):
        for newspaper in editor.newspaper_list:
            for editorr in self.editors:
                if newspaper in editorr.newspaper_list:
                    editorr.issue_list.append(editor.issue_list)
        self.editors.remove(editor)

    def add_subscriber(self, new_subscriber: Subscriber):
        self.subscribers.append(new_subscriber)

    def get_subscriber(self, subscriber_id:int) -> Optional[Subscriber]:
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                return subscriber
        return None

    def all_subscribers(self) -> List[Subscriber]:
        return self.subscribers

    def remove_subscriber(self, subscriber: Subscriber):
        for newspaper in self.newspapers:
            for paper in subscriber.subed_to:
                if newspaper == paper:
                    newspaper.subs.remove(subscriber)
        self.subscribers.remove(subscriber)

    
    def all_issues(self, paper_id:int):
        paper = self.get_newspaper(paper_id)
        if paper is not None:
            return paper.issues
        else:
            raise ValueError("The newspaper with ID", paper_id, "does not exist.")

    def add_issue(self,new_issue: Issue, paper_id:int):
        paper = self.get_newspaper(paper_id)
        paper.issues.append(new_issue)
        return new_issue

    def issue_info(self, issue_id, paper_id):
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for issue in paper.issues:
                    if issue.issue_id == issue_id:
                        return issue
        return None
    
    def remove_issue(self, issue_id, paper_id):
        issue = self.issue_info(issue_id, paper_id)
        paper = self.get_newspaper(paper_id)
        paper.issues.remove(issue)
        return None
                    
    def release_issue(self,issue_id:int,paper_id:int):
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                for issue in paper.issues:
                    if issue.issue_id == issue_id:
                        issue.released = True
                        return issue
        return None
        
    def set_editor1(self, issue_id: int,paper_id:int, editor_id:int):
        issue = self.issue_info(issue_id, paper_id)
        for editor in self.editors:
            if editor.editor_id == editor_id:
                issue.set_editor(editor)
                editor.issue_list.append(issue)
                return editor.issue_list
        return None
    
    def set_editor2(self,paper_id, editor_id):
        paper = self.get_newspaper(paper_id)
        for editor in self.editors:
            if editor.editor_id == editor_id:
                paper.set_editor(editor)
                editor.newspaper_list.append(paper)
                return editor.newspaper_list
        return None
    
   
    def get_editor_issues(self, editor_id:int):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor.issue_list
        return None           

    def subscribe_to(self, paper_id:int, subscriber_id:int):
        paper = self.get_newspaper(paper_id)
        sub = self.get_subscriber(subscriber_id)
        sub.sub_to(paper)
        sub.subed_to.append(paper)
        paper.subs.append(sub)
        return sub.subed_to
    
    def deliver(self,paper_id:int,issue_id:int, subscriber_id:int):
        issue = self.issue_info(issue_id, paper_id)
        paper = self.get_newspaper(paper_id)
        subscriber = self.get_subscriber(subscriber_id)
        if issue in subscriber.special_issues:
            if issue.released == True:
                subscriber.issue_recieved.append(issue)
                return subscriber.issue_recieved
        elif issue in paper.issues:
            if issue.released == True:
                if paper in subscriber.subed_to:
                    subscriber.issue_recieved.append(issue)
                    return subscriber.issue_recieved
                
    
    def get_issues_of_editor(self,editor_id):
        editor = self.get_editor(editor_id)
        if editor is not None:
            return editor.issue_list
        else:
            raise ValueError("The editor with ID", editor_id, "does not exist.")
        
    def subscribe_to_special_issue(self, paper_id:int, subscriber_id:int, issue_id:int):
        issue = self.issue_info(issue_id, paper_id)
        sub = self.get_subscriber(subscriber_id)
        sub.special_issues.append(issue)
        return sub.special_issues
    
    def missing_issues(self, subscriber_id: int):
        search_result = self.get_subscriber(subscriber_id)
        if search_result is None:
            raise ValueError(f"Subscriber with id {subscriber_id} does not exist")
    
        for issue in search_result.special_issues:
            if issue not in search_result.issue_recieved and issue.released:
                search_result.missing_issues.append(issue)
    
        for paper in search_result.subed_to:
            for issue in paper.issues:
                if issue.released and issue not in search_result.issue_recieved:
                    search_result.missing_issues.append(issue)
    
        return search_result.missing_issues
        
    def get_stats(self, paper_id:int):
        stats = {}
        paper = self.get_newspaper(paper_id)
        number_of_subscribers = len(paper.subs)
        monthly_revenue = number_of_subscribers * paper.price
        annual_revenue = monthly_revenue*12
        stats.update({'number_of_subscribers':number_of_subscribers,'monthly_revenue':monthly_revenue, 'annual_revenue':annual_revenue})
        return stats
    
    def subscriber_stats(self, subscriber_id:int):
        subscriber = self.get_subscriber(subscriber_id)
        monthly_cost = 0
        for paper in subscriber.subed_to:
            monthly_cost += paper.price
        for issue in subscriber.special_issues:
            monthly_cost += issue.price
        annual_cost = monthly_cost*12
        number_of_issues = {}
        counter = 0
        for paper in subscriber.subed_to:
            for issue in paper.issues:
                if issue in subscriber.issue_recieved:
                    counter += 0
                    number_of_issues.update({paper.paper_id:counter})
        return monthly_cost, annual_cost, number_of_issues


