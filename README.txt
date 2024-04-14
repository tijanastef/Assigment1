Programming Assignment 1
I left comments in my code as well but documenting my code helped me keep track of what I did.
There are some notes and explanations on how I understood and approached different tasks.
| `/newspaper`                                     | `GET`       | List all newspapers in the agency.   
tested (Agency)                                                                                                                
| `/newspaper`                                     | `POST`      | Create a new newspaper.                                                                                                                                 When creating a new newspaper, editor, subscriber, or issue a unique ID is assigned using a timestamp. The timestamp takes the time in milliseconds so it is always unique, I did this by importing time. (Might not be the best way possible to assign an ID in real life, but it works well for the project. Using IDs from databases is the best solution, but I wanted to be creative.) The ID is not required, even if it is written while creating a new object it will get overwritten by the timestamp.
tested (Agency)
| `/newspaper/<paper_id>`                          | `GET`       | Get a newspaper's information.     
Using the ID of the newspaper I go through a list of newspapers in the agency and find a match, return the information. If it does not exist a value error message appears.
Tested (Agency)
| `/newspaper/<paper_id>`                          | `POST`      | Update a new newspaper.                                                                                                                                 
When updating I made it so you can choose to update only one attribute or more. I am also tracking if a change was even made or not, if not an error appears.
| `/newspaper/<paper_id>`                          | `DELETE`    | Delete a newspaper, and all its issues.                                                                                                                 The issues are deleted along with the newspaper.
Tested (Agency)
| `/newspaper/<paper_id>/issue`                    | `GET`       | List all issues of a specific newspaper.               
Tested (Agency)                                                                                                 
| `/newspaper/<paper_id>/issue`                    | `POST`      | Create a new issue.                                                                                                                                     
When creating an issue I ask for the newspaper ID so I can make the issue inside of the newspaper and append it to the list of issues that the newspaper has as an attribute. 
When creating a new issue the “released” attribute is set to False. Even if you write down True while trying to create it, it will still keep it set to False.
Tested (Agency)
| `/newspaper/<paper_id>/issue/<issue_id>`         | `GET`       | Get information of a newspaper issue        
 Tested (Agency)
| `/newspaper/<paper_id>/issue/<issue_id>/release` | `POST`      | Release an issue                                                                                                                                        
The method changes the “released” attribute to “True”. It uses the paper ID and issue ID to find the issue and just changes the Boolean from False to True with the method in the agency file.
Tested (Agency)
| `/newspaper/<paper_id>/issue/<issue_id>/editor`  | `POST`      | Specify an editor for an issue. (Transmit the editor ID as parameter)     
The editor has a list of issues for which he is responsible and this is a method to assign the editor to an issue, in that method I append the issue to the editor's list of issues as well as set the editor for the issue with editor ID. I return the list of issues from the editor.
| `/newspaper/<paper_id>/issue/<issue_id>/deliver` | `POST`      | "Send" an issue to a subscriber. This means there should be a record of the subscriber receiving                              
I append the delivered issue to the list in “subscriber” only if the issue has been released. Works for both special issues and issues of a newspaper that the subscriber is subscribed to.
Tested (Agency)
| `/newspaper/<paper_id>/stats`                    | `GET`       | Return information about the specific newspaper (number of subscribers, monthly and annual revenue)
Because this is specifically for newspapers, it does not include special issues.
Tested (Agency)
| `/editor`                                        | `GET`       | List all editors of the agency.            
tested (Agency)                                                                                                           
| `/editor`                                        | `POST`      | Create a new editor.                                                                                                                                    
Tested (Agency)
| `/editor/<editor_id>`                            | `GET`       | Get an editor's information.                                                                                                                            Tested (Agency)
| `/editor/<editor_id>`                            | `POST`      | Update an editor's information.                                                                                                                         |
| `/editor/<editor_id>`                            | `DELETE`    | Delete an editor.                                                                                                                                       
Tested (Agency)
| `/editor/<editor_id>/issues`                     | `GET`       | Return a list of newspaper issues that the editor was responsible for.                                                                                  
| `/subscriber`                                    | `GET`       | List all subscribers in the agency.                                                                                                                     
Tested (Agency)
| `/subscriber`                                    | `POST`      | Create a new subscriber.                                                                                                                                
Tested (Agency)
| `/subscriber/<subscriber_id>`                    | `GET`       | Get a subscriber's information.                                                                                                                         
Tested (Agency)
| `/subscriber/<subscriber_id>`                    | `POST`      | Update a subscriber's information.                                                                                                                      |
| `/subscriber/<subscriber_id>`                    | `DELETE`    | Delete a subscriber.                                                                                                                                    
Tested (Agency)
| `/subscriber/<subscriber_id>/subscribe`          | `POST`      | Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as parameter.)          
To do this I needed to create a ‘paper_id_model’ and use payload for it.
I make two lists, one inside newspaper, and one inside subscriber.
The list inside subscriber has all the newspapers it is subscribed to,
The list inside the newspaper has all its subscribers inside.
Tested (Agency)
'/<int:subscriber_id>/subscribe/<int:paper_id>/<int:issue_id>'
When making a subscribe method for special issues I decided to use this route.
Because it wasn’t a specified method I didn’t have to transmit the paper ID, this way I avoided using a model again and made it easier.
Tested (Agency)
| `/subscriber/<subscriber_id>/stats`              | `GET`       | Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper. |  
The monthly and annual costs are for all newspapers and special issues the subscriber is subscribed to, keeping in mind that a special issue has a special price(I added that attribute to the issue class). And “the number of issues that the subscriber received for each paper” is just for the newspaper the subscriber is subscribed to.
That is how I understood it.
| `/subscriber/<subscriber_id>/missingissues`      | `GET`       | Check if there are any undelivered issues of the subscribed newspapers.        

                                     
Update issue:
Here you can change only the number of pages and release date. Everything else is covered with different methods. If no changes were made an error message appears.
Special issues! @subscriber_ns.route('/<int:subscriber_id>/subscribe/<int:paper_id>/<int:issue_id>')
A special issue is just one specific issue to which the subscriber can subscribe without subscribing to the whole newspaper. There is a post method for subscribing a subscriber to the special issue and it takes in subscribers, newspapers, and issues IDs so we can make sure we are taking the right issue. The issue is stored in a list inside of the subscriber so we can keep track and later deliver it. 
Tested (Agency)

•	I stored the classes ‘subscriber’, ‘newspaper’, and ‘issues’ in separate files at first but later I had to store them in the same file to solve the circular import error.
•	I used error messages where I found them necessary.
•	When deleting a newspaper all issues are deleted.
•	When a client is removed (e.g., cancels a subscription), all subscriptions are stopped.
•	When deleting an editor I transfer all issues in his/her supervision to another editor of the same newspaper.
•	A subscriber can subscribe to only one issue of a newspaper(special issue) or to the whole newspaper.
•	An editor can be set for an issue or the whole newspaper(set_editor1, set_editor2).
•	I made one test for each method in agency and as many as I could in testNS.
