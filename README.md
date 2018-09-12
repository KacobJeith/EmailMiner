# EmailMiner
This script is an attempt to automate the excruciating process of searching for relevant email addresses. 

At present, the script grabs profiles from a Houzz webpage query, and collects all websites that are linked from the Houzz profiles. The script then visits each website, and performs an exhaustive search throughout the main page, and any immediate subdirectory links referencing the words ['team', 'about', 'contact', or 'people']. 

## Usage

1. Call the script from command line using `python MineEmails.py [city] [state abbreviation] [number of pages to search]` 
2. Results are saved in a subdirectory "results", in a file named "city--state.csv"
