from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort

import time

from ..model.agency import Agency
from ..model.newspaper import Editor

from ..api.newspaperNS import issue_model

editor_ns = Namespace("editor", description="Editor related operations")

editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=False,
            help='The unique identifier of a editor'),
    'name': fields.String(required=True,
            help='The name of the editor.'),
    'address': fields.String(required=True,
            help='Address of the editor'),
   })


@editor_ns.route('/')
class EditorAPI(Resource):

    @editor_ns.doc(editor_model, description="Add a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        editor_id = int(time.time() * 1000)

        new_editor = Editor(editor_id=editor_id,
                              name=editor_ns.payload['name'],
                              address=editor_ns.payload['address'])
        Agency.get_instance().add_editor(new_editor)

        return new_editor

    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return Agency.get_instance().all_editors()


@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
 
    parser = reqparse.RequestParser()
    #the id is not included because we are just updating an already exsiting editor, 
    #the list of the newspaper and issues he is responsible for is also not included because i made a seperate function for that
    parser.add_argument('name', type=str, required=False, help="Name of the editor")
    parser.add_argument('address', type=str, required=False, help="Address of the editor")

    @editor_ns.doc(description="Get a new editor")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        if search_result is not None:
            return search_result
        else:
            abort(401, message=f"Editor with ths id does not exist")

    @editor_ns.doc(description="Update an editor")

    @editor_ns.expect(parser, validate=False) 
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self, editor_id):
        arguments = self.parser.parse_args()

        search_result = Agency.get_instance().get_editor(editor_id)
        #in case an the id is not valid
        if not search_result:
            abort(401, message=f"No editor with ID {editor_id} found")

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

    @editor_ns.doc(description="Delete a new editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_newspaper(editor_id)
        if not targeted_editor:
            abort(400, 'Editor was not found')
        Agency.get_instance().remove_editor(targeted_editor)
        return jsonify(f"Editor with ID {editor_id} was removed")

@editor_ns.route('/<int:editor_id>/issues')
class EditorIssue(Resource):
    @editor_ns.doc(description="Get a list of issues the editor is responsible for")
    @editor_ns.marshal_with(issue_model, envelope='issue')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor_issues(editor_id)
        if search_result is not None:
            return search_result
        else:
            abort(401, message=f"Editor with ths id does not exist")
