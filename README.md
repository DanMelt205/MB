# MB

#Applicaiton Domain Accounting

  -Sprint1 - Feature list for User Interface Module:  
    
    [] The login username, picture, should be displayed clearly on the top right corner of the login page once they have successfully logged into the system;
        - User can not upload their own picture. 

    [] The create a new user button will be used if the user is accessing the system for the first time. Clicking this button should display a user interface where the user will provide personal information such as first name, last name, address, DOB, and click submit to request access to the application.The administrator should receive email request and must approve or reject the request. If approved, an email should be sent to the user with a
      link to login to the system;
        - No email sent once for user approval, admin has to make account active in order for user to login.

  -Sprint2 - Chart of Accounts Module Feature List:

    [] The name of the logged user must be shown on the top left corner of the page;
        - Conflicts with sprint one easy switch.

    [] Each button must have a built-in tool-tip providing information about the purpose of the control;
        - No tool tips added at the moment.

    [] Each page must have a help button having information about the entire software organized by topic;
        - Faqs page added not sure if that will suffice. 



  -Sprint3 - Feature list Journalizing and Ledger Module

    Manager user:
      [] The ledger page must have filtering and search features.  You need to allow filtering by date or date range, and be able to search by account name or amount;
        - Not sure of what is meant the ledger is more of a sheet for viewing.

    Accountant user:
      [] Manager must get notification when journal entry is submitted for approval;
        - Havent thought out the entire process of this. Could simply email all managers.

  -Sprint4 – Adjusting entries and financial Reports Feature List

    Manager user:
      [] Can generate, view, save, email, or print trial balance, income statement, balance sheet, and retained earnings statement for a particular date or a date range.
        - All is implemented not sure about the retained statement. Making an assumption that it is an equity subcatagory. 
        - Actual statments need to be formated and designed better.

  -Added data few issues with design and input
  
      [] Number currency with negative number infront.
        - Possibly could fix but might cause different output than the correct at the moment.
        - Trail Balance page needs work on the total of debit and of credits section.
        - Not to mobile friendly in certain areas formating is off.

  -Sprint5 - Financial Ratios and Dashbord Feature List
  
      [] A section of the landing page can also be used to display important messages such as if there are 
        journal entries waiting for approval, etc.
          -Dashboard needs to be designed better. Could not find inspiration for the dashboard in accounting, that was simple enough to create or edit.
