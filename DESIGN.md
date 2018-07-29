[00:17, 12/7/2017] Bia Marinho: Design Documentation for Harvard Geneds:

MISSION:

The idea of our final projet came when we were discussing classes we would be taking during our next semester. The three of us
still have many general education categories to fulfill and we were unsure about which classes which we should take and which
classes are actually available to fulfill these requirements. We noticed that there was no single organized databse or website which
displayed the classes for specific general education requirements and so we decided to tackle this problem.

We aim to solve the frustrating and confusing experience that Harvard College students have to go through when they are thinking
about planning their next semesters (or even future academic years) and have no idea which classes they need to take to complete the
general education requirements they need to graduate.


WHY A WEBSITE?

The easiest and most efficient we found of displaying this information was as a website. We surveyed many Harvard students and
discovered that the majority conducts the process of choosing their classes through web-based platforms such as my.harvard and the Q
guide. As such, it made complete sense for our platform to be web-based in order to be of easy access when students are going
through this process.

We also noticed that, due to the large amount of classes that fulfill general education requirements, implementing this project via
an app would not be the best way for the user to visualize the large amount of data.


FOUNDATION:

After having completed all the course's problem sets, we thought the distribution code from Problem Set 7 (Finance) really resonated
with our idea. We then began by using it as a base, deleting all the unnecessary information associated specifically with Finance
and basically using the HTML and CSS as a first step to beginning our project.


IMPLEMENTATION & DESIGN:

The actual first step of our project was getting already existing information from the CS50 Courses API, which we required from the
CS50 course heads in order to implement the project. This information came to us in the form of a SQL table, which contained data
about classes, instructors, Q scores, amongst others.

Our next step was to manually go to my.harvard.edu. Using the Advanced Search function, we individually went through each general
education category and developed our own CSV file with a table containing classes and the general education requirements they
fulfilled. We of course had to account for classes that completed more than one requirement. This was an important design decision
as we struggled to determine which was the most efficient way to perform the separation of classes with multiple geneds, and we
decided to have three separate columns for each general education requirements that one class could fulfill (seeing that three
requirements was the maximum number found).

Another important decision we had to make was how to link the SQL table we already had to the one we were creating with general
education requirements information. The way we chose to solve this problem was to have a primary key (a course ID) that was already
provided in the CS50 Courses SQL table, and add a new column to our own table pairing classes according to this course ID.

We then imported this CSV file into PhpLiteAdmin and thus had all the information we needed to begin coding. The most essential part
of our code combined Python, SQL, HTML and Jinja. First, in application.py we perform a SQL command to extract from the table
classes that fulfilled the boxes (general education requirements they have to fulfill) our user had selected in the webpage and
combining each class with its respective Qscore found in another table. This was done through a forloop which allowed to perform
this operation for each category selected.

We then returned a HTML page (using render_template), that, using Jinja, was able to display all the classes with their overall Q
scores beside them, all under their specific categories in a table format.