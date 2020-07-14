# Bank Statement Analysis

<h3> Some Screen Captures </h3>
![Screen Capture](https://user-images.githubusercontent.com/47830627/87480643-a60a3d80-c625-11ea-9672-b2223292a9db.PNG)
<br><br>
![Screen Capture](https://user-images.githubusercontent.com/47830627/87480712-ce923780-c625-11ea-8d3c-b4fd0a0b6ac0.PNG)

<h3> What is this project about ? </h3>
This project composed of two section, analysis bank statement data and a web interface to show the analysised data and edit records.
<br>
<h4>Section 1: Analysis Bank Statement Data (Data preparation for the web interface)</h4>
This project is built based on two csv files of bank statement, tranhist.csv & midata.csv, available from HSBC online bank service. <br>
Thw whole preparation process:<br>
Step 0: Download the csv files from the HSBC website and install the required modules (full list at lower section).<br>
Step 1: Put the midata.csv and tranhist.csv file in the statement folder.<br>
Step 2: Run the midata.py file, copy the result (./statement/midata_tranhist.csv) and paste it to the bottom of tranhist.csv.<br>
(Optional Step: update categoriesjson in category.py to fit your record better)<br> 
Step 3: Set up your own MySQL local/global database and table (creating table command is available in dbInput.py) <br>
Step 4: Update the dbconfig.py with your login credentials.<br>
Step 5: Run the dbInput.py file. (uncomment the insert line)<br>


<h4> Section 2:Web interface</h4>
All you need to do is run ./server/app.py and access the corresponding localhost url :) <br>

<h3>Required Python Modules </h3>
<ul><li>Flask</li>
<li>MySQL connector</li></ul><br>
Basic MySQL knowledge and MySQL are required as you have to build your own database table. 
