# **HSGMemeGame**

## **General information**
Course: 7,789 | 8,789: Skills: Programming with Advanced Computer Languages  
Professor: Mario Silic  
University: University of St.Gallen (HSG)  
Authors: Wanja Butz, Jan Ewenz Rocher, Adrian Pandjaitan  
Date: 20.05.2021  
## **Background**
The following project is a submission of a student team (see authors) as part of the decentral examination of the course (see Course). For this, the team sought to take on a project which meets the requirements of the course and which is interesting enough to be pursued beyond the end of the course.  
For this, we chose the HSG Meme Game, which is a game for students of the University of St.Gallen. It's a fun activity based on jokes centered around the university, it's chlichées and the student life around it. 
## **Game rules**
Every player has 6 text cards on their hand. Each round one of the players is a judge and the others are players. For each round one meme is shown on the screen and each one of the players is putting a text card which they believe is funniest to that particular meme. Then the judge sees all the text cards and picks the funniest one which is also the winner card. The player to first win as many rounds as required by the winning points has won the game.  
The detailed game rules can be viewed in the seperate Game rules file.
## **Installation & running**
In order to execute the program, please follow these steps:
1) Download the git repository as a .zip file
2) Unzip it to your desired location
3) Access your computer's terminal 
5) Install django (in case you haven't installed it already, please follow this documentation: https://docs.djangoproject.com/en/1.8/howto/windows/#:~:text=Django%20can%20be%20installed%20easily,version%20in%20the%20command%20prompt.)
6) Change the directory to the game path in the terminal
7) Execute python manage.py makemigrations core
8) Execute python manage.py migrate
9) Execute python manage.py createsuperuser and klick through the process
10) Execute python manage.py runserver
11) Copy the generated link and paste it into your browser, this will start the game
- Add "/game" to the end of the link to access and play the game
- Add /admin to the end of the link to access the admin panel
## **Technical implementation - Overview**
The project consists of two main elements: the backend and the frontend.
### **1) The backend**
The backend includes the game logic, programmed in python. Also, here we access the various memes stored as .png and .gif files and the text cards stored as a .csv file.  
We then access these files and distribute them throughout the game. We store the variables per player and keep counting them throughout the game. For our web framework, we use django which is a high-level Python Web framework that is frequently used in rapid development environments due to its clean design and easy usability. 
In particular the backend includes the following files:
-**HSGMemeGame-main\core**
- View.py: A view is a request handler function, which receives HTTP requests and returns HTTP responses. Views access the data needed to satisfy requests via models, and delegate the formatting of the response to templates. 
- Models.py: Models are Python objects that define the structure of an application's data, and provide mechanisms to manage (add, modify, delete) and query records in the database. We follow the django coding approach "build fat models and slim views" in the models.py and views.py.
- URLs.py: A URL mapper is used to redirect HTTP requests to the appropriate view based on the request URL. The URL mapper can also match particular patterns of strings or digits that appear in a URL and pass these to a view function as data.  
- \media: Here we store the text cards as well as the memes which we then call during the game
- \static\core: This folder we need for any media elements that are part of the game (e.g., our placeholder example image) and are not replacable 
- \migrations: This folder connects the database with the game / app. We initiate it in the installation process (see above).
-**HSGMemeGame-main\**
- \hsgmemegame: Here we further define some settings as well as other elements required for the django framework.
- db.sqlite3: This is the database for the cards and the players
### **2) The frontend**
The frontend is coded in HTML and CSS. It creates the visual elements and the site with which the users can engage.  
The frontend consists of XX different screens which are all relevant to the game. On each site there are buttons and other elements with which the users can interact to steer the flow of the game.   
The frontend includes the following files:  
-**HSGMemeGame-main\core\templates\core**
- All the files in this folder create the visual elements that will later be seen in the game. We used HTML and CSS for the coding of these visualisations. 
