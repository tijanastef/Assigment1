from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort

import time

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.newspaper import Issue

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")


paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })

issue_model = newspaper_ns.model('IssueModel', {
    'issue_id': fields.Integer(required=False,
            help='The unique id of the issue'),
    'number_of_pages': fields.Integer(required=True,
            help='The number of pages the issue has'),
    'releasedate': fields.String(required=True,
            help='The date of the issue release'),
    'price': fields.Integer(required=True,
            help='The price of the special issue'),
    'released': fields.Boolean(required=True,
            help='Information is it yet released or not')
})

editor_id_model = newspaper_ns.model('EditorIdModel', {
    'editor_id': fields.Integer(required=True,
            help='The id of the editor')
   })

subscriber_id_model = newspaper_ns.model('SubscriberIdModel', {
    'subscriber_id': fields.Integer(required=True,
            help='The id of the subscriber')
   })

@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        paper_id = int(time.time() * 1000)

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper
    @newspaper_ns.doc(description="List all newspapers")
    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()
    
   
@newspaper_ns.route('/<int:paper_id>/stats')
class PaperStats(Resource):
    @newspaper_ns.doc(description="Get a paper stats")
    def get(self, paper_id):
        try:
            search_result = Agency.get_instance().get_stats(paper_id)
            return jsonify(search_result)
        except ValueError:
            abort(400, "Something went wrong.")



@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('name', type=str, required=False, help="Name of the newspaper")
    parser.add_argument('frequency', type=int, required=False, help="Frequency of the newspaper in days")
    parser.add_argument('price', type=int, required=False, help="Monthly price of the newspaper")

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        if search_result is not None:
            return search_result
        else:
            abort(401, message=f"Newspaper with ths id does not exist")


    @newspaper_ns.doc(description="Update a new newspaper")

    @newspaper_ns.expect(parser, validate=False)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            abort(401, message=f"No newspaper with ID {paper_id} found")


        updated = False
        
        if arguments['name'] is not None:
            search_result.name = arguments['name']
            updated = True
        if arguments['frequency'] is not None:
            search_result.frequency = arguments['frequency']
            updated = True
        if arguments['price'] is not None:
            search_result.price = arguments['price']
            updated = True

        if not updated:
            abort(401, message=f"No updates have been made")


        return search_result

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            abort(400, 'Newspaper not found')
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
    
@newspaper_ns.route('/<int:paper_id>/issue')
class IssueAPI(Resource):
    @newspaper_ns.doc(issue_model, description="Create a new issue")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        issue_id = int(time.time() * 1000)

        new_issue =Issue(issue_id=issue_id,
                            number_of_pages=newspaper_ns.payload['number_of_pages'],
                            releasedate=newspaper_ns.payload['releasedate'],
                            price = newspaper_ns.payload['price'],
                            released=False)
        Agency.get_instance().add_issue(new_issue, paper_id)
        return new_issue

    @newspaper_ns.marshal_list_with(issue_model, envelope='issues')
    @newspaper_ns.doc(issue_model, description="Get all issues from a newspaper")
    def get(self, paper_id):

        search_result = Agency.get_instance().all_issues(paper_id)
        return search_result

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class IssueId(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('number_of_pages', type=str, required=False, help="Number of pages issue has")
    parser.add_argument('releasedate', type=str, required=False, help="releasedate of the issue") 
    parser.add_argument('price',type = int, required= False, help='Price of the special issue')

    @newspaper_ns.marshal_list_with(issue_model, envelope='issues')
    @newspaper_ns.doc(issue_model, description="Get information for an issue using the issue id")
    def get(self, issue_id, paper_id):
        issue =Agency.get_instance().issue_info(issue_id, paper_id)
        if issue is not None:
            return issue
        else:
            abort(401, message=f"Issue with ths id does not exist")
    
    @newspaper_ns.doc(description="Update an issue")
    @newspaper_ns.expect(parser, validate=False)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, issue_id, paper_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().issue_info(issue_id, paper_id)
        if not search_result:
            abort(401, message=f"No issue with ID {issue_id} found")

        updated = False

        if arguments['number_of_pages'] is not None:
            search_result.number_of_pages = arguments['number_of_pages']
            updated = True
        if arguments['releasedate'] is not None:
            search_result.releasedate = arguments['relesedate']
            updated = True
        if arguments['price'] is not None:
            search_result.releasedate = arguments['price']
            updated = True

        if not updated:
            abort(401, message=f"No updates have been made")

        return search_result

    @newspaper_ns.doc(description="Delete an issue")
    def delete(self, issue_id, paper_id):
        Agency.get_instance().remove_issue(issue_id, paper_id)
        return jsonify(f"Issue with ID {issue_id} was removed")


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class IssueRealse(Resource):
    @newspaper_ns.doc(issue_model, description="Release an issue")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self, issue_id, paper_id):
        result = Agency.get_instance().release_issue(issue_id, paper_id)
        return result

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class EditorAPI(Resource): 
    @newspaper_ns.doc(issue_model, description="Assign an editor to an issue")
    @newspaper_ns.expect(editor_id_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self,issue_id, paper_id):
        editor_id = newspaper_ns.payload['editor_id'] 
        issue = Agency.get_instance().set_editor1(issue_id, paper_id, editor_id)
        return issue

@newspaper_ns.route('/<int:paper_id>/editor')
class EditorAPI2(Resource): 
    @newspaper_ns.doc(paper_model, description="Assign an editor to a newspaper")
    @newspaper_ns.expect(editor_id_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self,paper_id):
        editor_id = newspaper_ns.payload['editor_id'] 
        issue = Agency.get_instance().set_editor2(paper_id, editor_id)
        return issue

@newspaper_ns.route('newspaper/<int:paper_id>/issue/<int:issue_id>/deliver')
class SendIssue(Resource):
    @newspaper_ns.doc(issue_model, description="Deliver an issue to a subscriber")
    @newspaper_ns.expect(subscriber_id_model, validate = True)
    @newspaper_ns.marshal_with(issue_model, envelope='issue')
    def post(self,paper_id, issue_id):
        subscriber_id = newspaper_ns.payload['subscriber_id']
        search_result = Agency.get_instance().deliver(paper_id,issue_id, subscriber_id)
        if search_result is not None:
            return search_result
        else:
            abort(401, message=f"Value Error")
        



