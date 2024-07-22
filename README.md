SQL File Analyzer

Overview

SQL File Analyzer is a Flask-based web application designed to analyze SQL files and provide insightful metrics about the contents. Users can upload SQL files through the web interface, and the application processes these files to count various elements such as the number of lines, comment lines, loops, and tables in SELECT statements. The results are displayed on the web interface, and users can download the Translated files and an Excel summary.

Features

	• File Upload: Allows users to upload SQL files through a simple web interface.
 
	• SQL Processing: Analyzes the uploaded SQL file to provide metrics such as:
	    1.	Total number of lines
	    2.	Number of comment lines
	    3.	Number of loops (WHILE statements)
	    4.	Number of tables in SELECT statements
 
	• Output Files: Generates and allows users to download:
	    1.  A text file with processed SQL statements
	    2.  An Excel file summarizing the analysis results
