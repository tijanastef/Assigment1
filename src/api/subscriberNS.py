from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort

import time
from typing import List
from ..model.newspaper import Issue
from ..model.agency import Agency
from ..model.newspaper import Subscriber
from ..api.newspaperNS import paper_model
from ..api.newspaperNS import issue_model

subscriber_ns = Namespace("subscriber", description="Subscriber related operations")

subscriber_model = subscriber_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='The name of the subscriber.'),
    'address': fields.String(required=True,
            help='Address of the subscriber'),
   })

paper_id_model = subscriber_ns.model('NewspaperIdModel', {
    'paper_id': fields.Integer(required=True,
            help='The unique identifier of a newspaper')})


@subscriber_ns.route('/')
class SubscriberAPI(Resource):

    @subscriber_ns.doc(subscriber_model, description="Add a new Subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        subscriber_id = int(time.time() * 1000)

        new_subscriber = Subscriber(subscriber_id=subscriber_id,
                              name=subscriber_ns.payload['name'],
                              address=subscriber_ns.payload['address'])
        Agency.get_instance().add_subscriber(new_subscriber)

        return new_subscriber

    @subscriber_ns.marshal_list_with(subscriber_model, envelope='subscribers')
    def get(self):
        return Agency.get_instance().all_subscribers()


@subscriber_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource):

    parser = reqparse.RequestParser()
    # The id is not included because we are just updating an already existing subscriber,
    # the list of the issues its subscriberd to is also not included because i have a method for that
    parser.add_argument('name', type=str, required=False, help="Name of the subscriber")
    parser.add_argument('address', type=str, required=False, help="Address of the subscriber")

    @subscriber_ns.doc(description="Get a new subscriber")
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def get(self, subscriber_id):
        search_result = Agency.get_instance().get_subscriber(subscriber_id)
        if search_result is not None:
            return search_result
        else:
            abort(401, message=f"Subscriber with ths id does not exist")

    @subscriber_ns.doc(description="Update a subscriber")
    @subscriber_ns.expect(parser, validate=False)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_subscriber(subscriber_id)
        # in case the id is not valid
        if not search_result:
            abort(401, message=f"No subscriber with ID {subscriber_id} found")

        updated = False

        if arguments['name'] is not None:
            search_result.name = arguments['name']
            updated = True
        if arguments['address'] is not None:
            search_result.address = arguments['address']
            updated = True

        if not updated:
            abort(401, message=f"No updates have been made")

        return search_result

    @subscriber_ns.doc(description="Delete a new newspaper")
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_newspaper(subscriber_id)
        if not targeted_subscriber:
            abort(400, 'Subscriber was not found')
        Agency.get_instance().remove_subscriber(targeted_subscriber)
        return jsonify(f"Subscriber with ID {subscriber_id} was removed")

    
@subscriber_ns.route('/<int:subscriber_id>/subscribe/<int:paper_id>/<int:issue_id>')
class SubscriberNewspaper(Resource):
    @subscriber_ns.doc(subscriber_model, description="Subscribe a subscriber to a special issue")
    @subscriber_ns.marshal_with(paper_model, envelope='subscribed_to')
    def post(self, subscriber_id, paper_id, issue_id):
        search_result= Agency.get_instance().subscribe_to_special_issue(paper_id, subscriber_id, issue_id)
        return  search_result
    

@subscriber_ns.route('/<int:subscriber_id>/stats')
class Stats(Resource):
    @subscriber_ns.doc(description="Get subscriber stats")
    def get(self, subscriber_id:int):
        return Agency.get_instance().subscriber_stats(subscriber_id)
        

@subscriber_ns.route('/subscriber/<int:subscriber_id>/missing_issues')
class SubscriberMissingIssues(Resource):
    @subscriber_ns.doc(description="List of missing issues")
    @subscriber_ns.marshal_with(issue_model, envelope='issues')
    def get(self, subscriber_id):
        return Agency.get_instance().missing_issues(subscriber_id)

@subscriber_ns.route('/subscriber/<int:subscriber_id>/subscribe')
class SubscriberNewspaper(Resource):
    @subscriber_ns.doc(paper_model, description="Subscribe a subscriber to a newspaper")
    @subscriber_ns.expect(paper_id_model, validate=True)
    @subscriber_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, subscriber_id):
        paper_id = subscriber_ns.payload['paper_id'] 
        result = Agency.get_instance().subscribe_to(paper_id, subscriber_id)
        return result
                               