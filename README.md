# sentimental_analysis_flask

Sentiment Analysis of Twitter comments, hashtags, or other data.
Output: Displayed in the form of a graph.
(Feel free to modify the content as needed.)



Steps 
1 --> Create a folder, for example, name it Flask.
2 --> open the folder in VS 
3 --> Open a new terminal and install the required libraries using the following commands:
      pip install flask
      pip install SQLAlchemy
      pip install bcrypt
      pip install textblob
      pip install matplotlib

4 --> Create the following subfolders in the Flask folder:
5 --> folder 
        -- templates
        -- static 
           -- image ( folder inside static )
6 --> make a file app.py ( this is your main file and its your backend part )
7 --> templates folder will have your front end part (html, css, .. files)
8 --> static -- image --> will have all the images linked with your html files 
9 --> train.py is model you are going to train ( modify accordingly as per your needs)
note other folders such as uploads, instance(database) will be created when you will run your project
10 --> output (plot) will be saved in folder uploads 

landing.html is your main page , which contain all the information
you have a registration page which will redirect you to the login page 
then you will a page, where you are going to upload your csv file for sentimental analysis and will have output there 

