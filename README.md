# bank-statement-analysis

<h3> What is this project about ? </h3>
This project composed of two section, analysis bank statement data and a web interface to show the analysised data and edit records.
<br>
<h4>Section 1: Analysis Bank Statement Data (Data preparation for the web interface)</h4>
This project is built based on two csv files of bank statement, tranhist.csv & midata.csv, available from HSBC online bank service. <br>
Thw whole preparation process:<br>
Step 0: Download the csv files from the HSBC website and install the required modules (full list at lower section).<br>
Step 1: Create a folder called statement in the root directory and put the midata.csv and tranhist.csv file in the statement folder.<br>
Step 2: Run the midata.py file and copy the result (./statement/midata_tranhist.csv) and paste it to the bottom of tranhist.csv.<br>
(Optional Step: update categoriesjson in category.py to fit your record better)<br> 
Step 3: Set up your own MySQL local/global database and table (creating table command is available in dbInput.py) <br>
Step 4: Run the dbInput.py file. (uncomment the insert line)<br>


<h4> Section 2:Web interface</h4>
All you need to do is run ./server/app.py and access the corresponding localhost url :) <br>

<h3>Required Modules </h3>
<ul><li>Flask</li>
<li>MySQL server</li></ul><br>
Basic MySQL knowledge is required as you have to build your own database table. 
