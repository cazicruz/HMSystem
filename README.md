Overview
HM System is a web based appointment booking system for hospitals that lets Patients book appointments with their doctors in a manner that is fully automated and simple.
This is developed with the Flask framework and accompanied with its own database to allow for new users to register on the platform, users would be able to book reschedule and cancel appointments 

Core Functionalities Explained

The problem that HM Systems tries to solve  is the difficulty and stress accompanied with paper file systems, where a patient would be in urgent need of healthcare but will be denied due to the difficulty in accessing his or her medical records.
Our intended users are large and medium sized health facilities be it hospitals , pharmacies, medical laboratories and lots more.

Architecture
The HM Systems MVP will consist of a web application with a front-end built using HTML, CSS, and JavaScript. The front-end will communicate with a back-end server built using Python and Flask web framework. The back-end will store data in a SQLite database.
The following is an end-to-end map for the data flowing through the system:
[User] —> interacts with —> [Front-end (HTML, CSS, JavaScript + Bootstrap)] 
					
communicates with [Django Web Framework] 
					
which interacts with [SQLite database]
APIs and Methods
API routes that will be created for the web client to communicate with the web server:
/
GET: returns the landing page with relevant details on products services etc.
/dashboard
GET: Returns the details of the specified ID(useer)
PUT: Updates the user details on appointments of the specified ID
DELETE: Deletes details of  the specified ID
/login
GET: Returns the login page 
POST: submits users credentials for verification and if valid redirects to the dashboard url
/sign-up
GET: Returns the sign-up page 
POST: submit the details submitted by the user and create an account for them if the account doesn't exist.
Data Modelling
The data model for the HM System MVP will consist of two tables: user  and roles. The user table will have the following fields:
id - IntegerField: A unique identifier for the topic.
text - CharField: The text description of the topic.
date_added - DateTimeField: The date the topic was added.
The roles table will have the following fields:
id - IntegerField: A unique identifier for the entry.
title- ForeignKey: The title of the role 


User Stories
User stories are short descriptions of a feature from an end-user's perspective. They are used to capture user requirements and describe the expected behavior of the system. A well-written user story should be specific, measurable, and testable. One pitfall to avoid when creating user stories is making them too general. User stories should be specific and focused on a particular task or goal. For example, instead of "As a user, I want the app to be easy to use," a more specific user story might be "As a beginner user, I want clear instructions on how to create a new topic."


Here are some user stories that could be used for the HM System:
As a patient i want to be able to book and cancel appointments easily
As a user, I want to be able to add entries to cancel a period on the clock to make it available to handle emergencies .

