#!/usr/bin/env python3
import http.cookiejar # For logging into LinkedIn
import csv # For creating the list of emails
import getpass # For getting the user's LinkedIn password securely
import json # For loading LinkedIn data
import math # For rounding up on the number of emails to get the number of pages
import os # For checking if cookie file is valid for logging into LinkedIn
import requests # For loading LinkedIn requests
import sys # For terminating the script with a status code from main
import time # For pausing every one second to wait for the output file to be closed if it is open before the script is run
import urllib # For logging into LinkedIn
import urllib3 # For logging into LinkedIn
import colorama
from bs4 import BeautifulSoup

# Initialize Colorama
colorama.init()

# Set the colors
bo = colorama.Style.BRIGHT
gr = bo + colorama.Fore.GREEN
bl = bo + colorama.Fore.BLUE
ye = bo + colorama.Fore.YELLOW
re = bo + colorama.Fore.RED
cb = bo + colorama.Fore.CYAN
wh = colorama.Fore.WHITE
en = colorama.Style.RESET_ALL

# Set the statuses
success = bo + gr + "[+] " + en
info = bo + bl + "[*] " + en
warning = bo + ye + "[-] " + en
failure = bo + re + "[!] " + en


# Print the banner
def print_banner():

    # Print the title
    print(gr)
    print(" ██████╗██╗ ██╗██╗██████╗██╗ ██╗  ██████╗ ██████╗███╗  ██╗ ".decode('utf8'))
    print(" ██╔═██║██║ ██║██║██╔═══╝██║ ██║  ██╔═══╝ ██╔═══╝████╗ ██║ ".decode('utf8'))
    print(" ██████║██████║██║██████╗██████║  ██║ ███╗████╗  ██╔██╗██║ ".decode('utf8'))
    print(" ██╔═══╝██╔═██║██║╚═══██║██╔═██║  ██║  ██║██╔═╝  ██║╚████║ ".decode('utf8'))
    print(" ██║    ██║ ██║██║██████║██║ ██║  ███████║██████╗██║ ╚███║ ".decode('utf8'))
    print(" ╚═╝    ╚═╝ ╚═╝╚═╝╚═════╝╚═╝ ╚═╝  ╚══════╝╚═════╝╚═╝  ╚══╝ ".decode('utf8'))
    print(en)

    # Set the offset
    offset = " " * 9

    # Set the details with 42 spaces
    line00 = "                                          "
    line01 = "                 PhishGen                 "
    line02 = "                                          "
    line03 = "     Phishing Email Address Generator     "
    line04 = "               Version: 1.0               "
    line05 = "                                          "
    line06 = "         Created by: James Morris         "
    line07 = "                                          "
    line08 = "      Visit: github.com/jamesm0rr1s       "
    line09 = "    Follow me on Twitter: @jamesm0rr1s    "
    line10 = "  Connect on linkedin.com/in/jamesm0rr1s  "
    line11 = "                                          "

    # Print the details
    print(offset + line00)
    print(offset + gr + line01 + en)
    print(offset + line02)
    print(offset + gr + line03[:10] + en + wh + line03[10:28] + en + gr + line03[28:31] + en + wh + line03[31:] + en)
    print(offset + wh + line04[:24] + en + wh + line04[24:] + en)
    print(offset + line05)
    print(offset + wh + line06[:21] + en + cb + line06[21:] + en)
    print(offset + line07)
    print(offset + wh + line08[:12] + en + gr + line08[12:] + en)
    print(offset + wh + line09[:25] + en + cb + line09[25:] + en)
    print(offset + wh + line10[:12] + en + gr + line10[12:] + en)
    print(offset + line11)


# Ask the user for the domain
def ask_user_for_domain():

    # Set a blank error message
    error_message = ""

    # Loop until a valid domain has been entered
    while True:
        # Ask the user to enter a domain
        domain = input("\n" + error_message + "Enter the domain. (example.com)" + "\n").lower()

        # Check if an incorrect domain was entered
        if "." not in domain:
            error_message = failure + "Incorrect domain entered. "

        # Correct domain entered
        else:
            return domain


# Ask the user for the output filename
def ask_user_for_output_filename(domain):

    # Ask the user for the output filename
    output_filename = input("\n" + "Enter a filename for the output. Leave blank to use \"emails-" + domain + ".csv\"" + "\n")

    # Check if no name was given
    if output_filename == "":
        output_filename = "emails-" + domain + ".csv"

    # A name was given
    else:
        # Print a blank line
        print("")

    # Check if a valid file extension was added by the user
    if output_filename[-4:] != ".csv":
        # Add the file extension
        output_filename = output_filename + ".csv"

    # Tell the user the filename
    print(info + "The list of emails will be saved as " + output_filename)

    # Return the filename
    return output_filename


# Check if the output file is open
def check_outputfile(filename, email_list):

    # Try to open the file
    try:
        # Test saving the header row to the file
        with open(filename, "wb") as fileOfEmails:
            csv_writer = csv.writer(fileOfEmails, quoting=csv.QUOTE_ALL)
            csv_writer.writerows(email_list)

    # File is open
    except:
        # Tell the user to close the file
        print("\n" + warning + "Close the file \"" + filename + "\"")

        # Loop until the file is closed
        while True:
            # Pause for one second
            time.sleep(1)

            # Try to open the file
            try:
                # Test saving the header row to the file
                with open(filename, "wb") as fileOfEmails:
                    csv_writer = csv.writer(fileOfEmails, quoting=csv.QUOTE_ALL)
                    csv_writer.writerows(email_list)

                # File write was successful
                break

            # File is open
            except:
                # Continue looping
                continue


# Open URL and get soup with cookie
def get_soup(url, opener=None, parameters=None):

    # Try to open the url
    try:        
        # Check if logging in with login parameters
        if opener and parameters:
            # Open the login page
            response = opener.open(url, parameters)

        # Not logging in
        elif opener:
            # Open the initial page
            response = opener.open(url)

        # Not for LinkedIn
        else:
            # Open the url
            response = urllib3.urlopen(url)

    # Catch exceptions
    except urllib3.URLError as e:
        # Tell the user that there was an error
        print("\n" + failure + "An error occured fetching " + url + " \n " + e.reason)
        # Return there was an error
        return "Error"

    # Return the soup
    return BeautifulSoup(response.read(), "html.parser")


# Get the email format
def get_email_format(domain):

    # Get the soup
    soup = get_soup("https://www.email-format.com/d/" + domain)

    # Set email format to blank in case it cannot be found
    email_format = ""

    # Get the first email format
    for div in soup.findAll("div", {"class": "format fl"}):

        # Set the email format
        email_format = div.text.strip()

        # Do not continue searching
        break

    # Return the email format
    if email_format == "first_name  . last_name":
        return "first.last"
    elif email_format == "first_name  last_name":
        return "firstlast"
    elif email_format == "first_initial  last_name":
        return "flast"
    elif email_format == "first_name  last_initial":
        return "firstl"
    elif email_format == "last_name  first_initial":
        return "lastf"
    elif email_format == "first_name":
        return "first"
    elif email_format == "last_name":
        return "last"
    else:
        return "Email format not found."


# Ask the user for the email format
def ask_user_for_email_format(domain):

    # Set a blank error message
    error_message = ""

    # Loop until a valid option has been selected
    while True:
        # Ask the user to select an email format
        email_format = input("\n" + error_message + "Select an email format. Leave blank to search for the format. (first.last, firstlast, flast, firstl, lastf, first, last)" + "\n").lower()

        # Check if no format was entered
        if email_format == "":

            # Tell the user that the email format is being searched for
            print(info + "Searching www.email-format.com for the email format")

            # Get the email format
            email_format = get_email_format(domain)

            # Check if the email format was found
            if email_format == "first.last" or email_format == "firstlast" or email_format == "flast" or email_format == "firstl" or email_format == "lastf" or email_format == "first" or email_format == "last":

                # Tell the user that the email format was found
                print("\n" + success + "Email format found: " + email_format)

                # Return the email format that was found
                return email_format
            
            # Email format was not found
            else:

                # Set the error message to email format not found
                error_message = warning + "The email format was not found. "

        # Check if a valid email format was selected
        elif email_format == "first.last" or email_format == "firstlast" or email_format == "flast" or email_format == "firstl" or email_format == "lastf" or email_format == "first" or email_format == "last":

            # Return the selected email format
            return email_format

        # Incorrect email format selected 
        else:

            # Set the error message to incorrect email format
            error_message = failure + "Incorrect email format entered. "


# Ask the user if they want to check LinkedIn for emails
def ask_user_to_generate_emails_from_linkedin():

    # Set a blank error message
    error_message = ""

    # Loop until a valid answer has been given
    while True:

        # Ask the user whether they want to also check LinkedIn
        checkLinkedin = input("\n" + error_message + "Would you like to generate emails from LinkedIn data? This "
                                                     "requires a username and password. (y/n)" + "\n").lower()

        # Check if the choice is yes
        if checkLinkedin == "y" or checkLinkedin == "yes":

            # Return yes
            return True

        # The choice is no
        elif checkLinkedin == "n" or checkLinkedin == "no":

            # Return no
            return False

        # Incorrect choice
        else:

            # Set the error message to incorrect choice entered
            error_message = failure + "Incorrect choice entered. "


# Ask the user for their LinkedIn email
def ask_user_for_linkedin_email():

    # Set a blank error message
    error_message = ""

    # Loop until a valid email has been entered
    while True:

        # Ask the user to enter their email
        linkedin_email = input("\n" + error_message + "What is your LinkedIn email address?" + "\n").lower()

        # Check if an incorrect email was entered
        if "@" not in linkedin_email and "." not in linkedin_email:

            # Set the error message to incorrect email entered
            error_message = failure + "Incorrect email entered. "

        # Correct email entered
        else:

            # Return the email
            return linkedin_email


# Ask the user for their LinkedIn password
def ask_user_for_linkedin_password():

    # Loop until a password has been entered
    while True:

        # Ask the user to enter their password
        linkedin_password = getpass.getpass(prompt="\n" + "What is your LinkedIn password?" + "\n")

        # Check if a blank password was entered
        if linkedin_password == "":

            # Set the error message to no password entered
            print(failure + "No password entered")

        # A password was entered
        else:

            # What's the harm in a little scare...
            print(info + "I got your password ;)   Kidding... check out the source code at https://github.com/jamesm" + gr + "0" + en + "rr" + gr + "1" + en + "s" + "\n")

            # Return the password
            return linkedin_password


# Login to LinkedIn
def login_to_linkedin(username, password):
    
    # Try to login to LinkedIn
    try:
        
        # Create a temporary file to store the cookie
        cookie_file = "cookie.txt"

        # Create a cookie jar for the HTTP cookies
        cookie_jar = http.cookiejar.MozillaCookieJar(cookie_file)

        # Check for file existence
        if os.access(cookie_file, os.F_OK):

            # Load the cookie jar file
            cookie_jar.load()

        # Create an url opener to add a cookie
        url_opener = urllib3.build_opener(
            urllib3.HTTPRedirectHandler(),
            urllib3.HTTPHandler(debuglevel=0),
            urllib3.HTTPSHandler(debuglevel=0),
            urllib3.HTTPCookieProcessor(cookie_jar)
        )

        # Add header
        url_opener.addheaders = [("User-agent", ("Mozilla/5.0"))]

        # Open the url with cookie
        #soup = get_soup("https://www.linkedin.com/", urlOpener) # No longer works as of July 2019
        soup = get_soup("https://www.linkedin.com/login", url_opener)

        # Get the csrf token
        #csrfToken = soup.find(id="loginCsrfParam-login")["value"] # No longer works as of July 2019
        csrf_token = soup.find("input", {"name":"loginCsrfParam"})["value"]

    # Set the login parameters
        login_parameters = urllib.urlencode({"session_key": username, "session_password": password, "loginCsrfParam": csrf_token})

        # Login to LinkedIn
        soup = get_soup("https://www.linkedin.com/uas/login-submit", url_opener, login_parameters)

        # Try to get the cookie
        try:

            # Get the li_at cookie
            cookie = cookie_jar._cookies[".www.linkedin.com"]["/"]["li_at"].value
            
        # Unable to get the cookie
        except:
            
            # Return nothing
            return None

        # Save the cookie jar file
        cookie_jar.save()

        # Remove the cookie file
        os.remove(cookie_file)

        # Check if there is not a cookie
        if len(cookie) == 0:
            
            # Return nothing
            return None

        # Tell the user that the login was successful
        print(info + "Successfully logged into LinkedIn")

        # Create a dictionary of cookies
        dictionary_of_cookies = dict(JSESSIONID="ajax:amFtZXNtMHJyMXM")

        # Add the li_at
        dictionary_of_cookies["li_at"] = cookie

    # Unable to login
    except:
        
        # Return nothing
        return None

    # Return the cookies
    return dictionary_of_cookies


# Ask the user for the LinkedIn company name to search for an ID
def ask_user_for_linkedin_company_name():

    # Set a blank error message
    error_message = ""

    # Loop until a company has been entered
    while True:

        # Ask the user to enter the company to search for
        company = input(error_message + "What company would you like to search LinkedIn for?" + "\n").lower()

        # Check if no company was entered
        if company == "":

            # Set the error message to no company entered
            error_message = failure + "No company name was entered. "

        # A company was entered
        else:

            # Return the company
            return urllib.quote_plus(str(company))


# Search for a company ID on LinkedIn using the company name
def get_company_id_from_linkedin(company_name, cookie_dict):

    # Create a list to store the company name and ID
    list_of_companies = []

    # Set the search url
    url = "https://www.linkedin.com/voyager/api/typeahead/hits?q=blended&query=" + company_name

    # Add v2 API headers
    v2headers = {"Csrf-Token":cookie_dict["JSESSIONID"], "X-RestLi-Protocol-Version": "2.0.0"}

    # Get the json data from the response
    json_data = json.loads(requests.get(url, cookies=cookie_dict, headers=v2headers).text)

    # Tell the user that companies are being searched for
    print("\n" + info + "Searching for companies using autocomplete \"" + company_name + "\"")

    # Loop through all of the elements
    for x in range(0, len(json_data["elements"])):

        # Try to get the company name and ID
        try:
            
            # Get the company name
            company_name = json_data["elements"][x]["hitInfo"]["com.linkedin.voyager.typeahead.TypeaheadCompany"]["company"]["name"]

            # Get the company ID
            company_id = json_data["elements"][x]["hitInfo"]["com.linkedin.voyager.typeahead.TypeaheadCompany"]["id"]

            # Add the company name and ID to the list of companies
            list_of_companies.append((company_name, company_id))

            # Tell the user that a company token was found
            print(success + "The company token found for \"" + company_name.encode("utf8") + "\" is " + company_id)

        # Error while getting company name and ID
        except:

            # Continue looping
            continue

    # Set the search url
    url = "https://www.linkedin.com/voyager/api/search/blended?keywords=" + company_name + "&origin=SWITCH_SEARCH_VERTICAL&count=10&q=all&filters=List(resultType->COMPANIES)&start=0"

    # Get the json data from the response
    json_data = json.loads(requests.get(url, cookies=cookie_dict, headers=v2headers).text)
    
    # Tell the user that companies are being searched for using a keyword
    print("\n" + info + "Searching for companies using keyword \"" + company_name + "\"")

    # Try to get the number of companies
    try:

        # Get the number of companies
        number_of_companies = len(json_data["elements"][0]["elements"])

        # Companies were found
        companies_found = True

    # No companies found
    except:

        # Companies were not found
        companies_found = False

    # Check if companies were found using the keyword search
    if companies_found:

        # Loop through all of the elements
        for x in range(0, number_of_companies):

            # Try to get the company name and ID
            try:
                
                # Get the company name
                company_name = json_data["elements"][0]["elements"][x]["title"]["text"]
                
                # Get the company ID
                company_id = json_data["elements"][0]["elements"][x]["trackingUrn"].split(":")[-1]
                    
                # Check if the company name and ID are not already in the list
                if (company_name,company_id) not in list_of_companies:

                    # Add the company name and ID to the list of companies
                    list_of_companies.append((company_name, company_id))

                    # Tell the user that a company token was found
                    print(success + "The company token found for \"" + company_name.encode("utf8") + "\" is " + company_id)

            # Error while getting company name and ID
            except:

                # Continue looping
                continue

    # Check if a company was found
    if list_of_companies:
        
        # Set the first company name found
        company_name = list_of_companies[0][0]

        # Set the first company ID found
        company_id = list_of_companies[0][1]

        # Tell the user which company name and ID are being used
        print("\n" + info + "The first company token found for \"" + company_name.encode("utf8") + "\" was: " + company_id)

        # Return the company ID
        return company_name, company_id

    # A company was not found
    else:

        # Return
        return ("-1", "-1")


# Ask the user for the LinkedIn company ID
def ask_user_for_linkedin_company_id(cookie_dict):

    # Set a blank error message
    error_message = ""

    # Loop until a valid integer has been entered
    while True:

        # Ask the user to enter the company ID
        linkedin_company_id = input("\n" + error_message + "What is the LinkedIn company ID? Leave blank to search for the ID." + "\n")

        # Check if the user wants to search for the company ID
        if linkedin_company_id == "":

            # Ask the user for the company name to search for
            companyToSearchForOnLinkedin = ask_user_for_linkedin_company_name()

            # Search LinkedIn for the company ID
            linkedinCompanyName, linkedin_company_id = get_company_id_from_linkedin(companyToSearchForOnLinkedin, cookie_dict)

            # Check if a company ID was not found
            if linkedin_company_id == "-1":

                # Set the error message to company ID not found
                error_message = warning + "Company ID not found. "

            # Company ID found
            else:
                
                # Set a blank error message for the main loop
                error_message = ""

                # Set an initial blank error message for the nested loop
                error_msg = ""

                # Loop until a valid integer has been entered
                while True:
        
                    # Check if the correct company was found
                    linkedin_company_correct = input("\n" + error_msg + "Would you like to select the company \"" + linkedinCompanyName + "\" with an ID of \"" + linkedin_company_id + "\" (y/n)" + "\n").lower()

                    # Check if the choice is yes
                    if linkedin_company_correct == "y" or linkedin_company_correct == "yes":

                        # Print a blank line
                        print("")

                        # Return the company ID
                        return str(linkedin_company_id)

                    # The choice is no
                    elif linkedin_company_correct == "n" or linkedin_company_correct == "no":

                        # Break out of the nested while loop
                        break

                    # Incorrect choice
                    else:

                        # Set the error message to incorrect choice entered
                        error_msg = failure + "Incorrect choice entered. "

        # User entered input
        else:

            # Check if input is was an integer
            try:

                # Check if ID can be casted to int, is not blank, and is greater than 0
                if int(linkedin_company_id) > 0:

                    # Print a blank line
                    print("")

                    # Return the company ID
                    return str(linkedin_company_id)

            # Input is not an integer
            except:
                
                # Set the error message to not an integer
                error_message = failure + "Input was not a valid integer. "


# Get the keywords search string for LinkedIn URLs
def get_search_string(keywordsForSearch):

    # Check if there are no keywords
    if keywordsForSearch == "":

        # Set the keywords search string to blank
        keywords_search_string = ""

    # There are keywords to search for
    else:
        
        # Set the keywords search string
        keywords_search_string = "&keywords=" + keywordsForSearch

    # Return the keywords search string
    return keywords_search_string


# Get the number of LinkedIn pages to search
def get_the_number_of_linkedin_pages_to_search(numberOfProfilesPerPage, keywordsForSearch, companyId, dictOfCookies):

    # Get the keywords search string
    keywords_search_string = get_search_string(keywordsForSearch)

    # Set the initial url to get the total number of pages
    url = "https://www.linkedin.com/voyager/api/search/cluster?count=" + str(numberOfProfilesPerPage)
    url += keywords_search_string + "&guides=List(v->PEOPLE,facetCurrentCompany->" + companyId
    url += ")&origin=OTHER&q=guided&start=0"

    # Add v2 API headers
    v2headers = {"Csrf-Token":dictOfCookies["JSESSIONID"], "X-RestLi-Protocol-Version":"2.0.0"}

    # Get the json data from the response
    jsonData = json.loads(requests.get(url, cookies=dictOfCookies, headers=v2headers).text)

    # Try to get data for the company
    try:
        
        # Get the total number of profiles
        totalProfiles = jsonData["elements"][0]["total"]

    # Company not found
    except:

        # Tell the user there were no results
        print(warning + "There were no search results for company ID \"" + companyId + "\" using the keywords \"" +
              keywordsForSearch + "\".")

        # Return since a company was not found
        return 0

    # Calculate the total number of pages rounding up to account for any profiles on the last page
    numberOfPagesToSearch = int(math.ceil(float(totalProfiles) / numberOfProfilesPerPage))

    # Check if there are more than 1,000 profiles
    if totalProfiles > 1000:

        # Limit to 1,000 profiles because this is the maximum that LinkedIn supports
        numberOfPagesToSearch = int(math.ceil(float(1000) / numberOfProfilesPerPage))

    # Return the number of pages
    return numberOfPagesToSearch


# Search LinkedIn for profiles
def search_linkedin_for_profiles(numberOfProfilesPerPage, numberOfPagesToSearch, keywordsForSearch, emailFormat,
                                 domainName, companyId, listOfPublicIdentifiers, listOfEmails, listOfUniqueEmails,
                                 dictOfCookies):

    # Get the keywords search string
    keywordsSearchString = get_search_string(keywordsForSearch)

    # Set the total number of page numbers
    pageNumbers = range(numberOfPagesToSearch)

    # Set the maximum page number
    maxPageNumber = max(pageNumbers) + 1
    
    # Loop through all of the pages
    for pageNumber in pageNumbers:

        # Check if there is not a keyword
        if keywordsForSearch == "":
        
            # Print the current search page
            print("\n" + info + "Searching LinkedIn page " + str(pageNumber + 1) + " of " + str(maxPageNumber))

        # There is a keyword
        else:

            # Print the current search page and keyword
            print("\n" + info + "Searching LinkedIn page " + str(pageNumber + 1) + " of " + str(maxPageNumber) +
                  " using the keyword \"" + keywordsForSearch + "\"")

        # Set the url using the page number
        url = "https://www.linkedin.com/voyager/api/search/cluster?count=" + str(numberOfProfilesPerPage) + keywordsSearchString + "&q=guided&guides=List(v->PEOPLE,facetCurrentCompany->" + companyId + ")&origin=OTHER&start=" + str(pageNumber * numberOfProfilesPerPage)

        # Add v2 API headers
        v2headers = {"Csrf-Token":dictOfCookies["JSESSIONID"], "X-RestLi-Protocol-Version":"2.0.0"}

        # Get the json data from the response
        jsonData = json.loads(requests.get(url, cookies=dictOfCookies, headers=v2headers).text)

        # Try to get profiles from the page
        try:

            # Get the profiles on the page
            profilesOnPage = jsonData["elements"][0]["elements"]

        # There were no profiles 
        except:

            # Check if there is not a keyword
            if keywordsForSearch == "":

                # Tell the user there were no profiles on the page
                print("\n" + warning + "No profiles found")

            # There is a keyword
            else:

                # Tell the user there were no profiles on the page
                print("\n" + warning + "No profiles found using the keyword \"" + keywordsForSearch + "\"" + "\n")

                # Return
                return

        # Loop through all of the profiles on the page
        for profile in profilesOnPage:

            # Create a blank warning string
            warningMessage = ""

            # Check if profile details are available
            if "com.linkedin.voyager.search.SearchProfile" in profile["hitInfo"] and not profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["headless"]:

                # Try to get public identifier
                try:

                    # Get the public identifier
                    publicIdentifier = "https://www.linkedin.com/in/" + str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["miniProfile"]["publicIdentifier"])

                # There was no public identifier
                except:

                    # Set a blank public identifier
                    publicIdentifier = ""

                # Check if the profile is already in the list and not blank
                if publicIdentifier in listOfPublicIdentifiers and publicIdentifier != "":

                    # Continue since the profile was already added
                    continue

                # Get the names
                firstNameRaw = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["miniProfile"]["firstName"].encode("utf8"))
                lastNameRaw = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["miniProfile"]["lastName"].encode("utf8"))

                # Get the first word of the names
                firstName = str(firstNameRaw.split()[0])
                lastName = str(lastNameRaw.split()[0])

                # Remove unwanted characters
                firstName = "".join([character if character.isalnum() else "" for character in firstName])
                lastName = "".join([character if character.isalnum() else "" for character in lastName])

                # Create a list of common titles
                listOfCommonTitles = ["Dr.", "Dr"]

                # Check if first word in first name is a title "Dr., Dr, "
                if firstName in listOfCommonTitles:

                    # Check if there was a second word in the first name
                    if len(firstNameRaw.split()) > 1:

                        # Update the first name with the second word in the first name
                        firstName = str(firstNameRaw.split()[1])

                    # First name is a title but there was not a second word in the first name
                    else:

                        # Tell the user that the first name was only one word and the word was a title
                        warningMessage += "The first name is a common title and there was"
                        warningMessage += "not a second word in the first name field. "

                # Create a list of common certificates
                listOfCommonCerts = ["AICP", "CSM", "SP", "CPA", "CIA", "CFE", "CFA", "CISA", "CISSP", "OSCP",
                                     "OSCE", "OSWP", "CEH", "Sec+", "Security+", "MBA", "MPA", "PMP", "PhD", "Ph.D.",
                                     "MA"]

                # Check if first word in last name is a common certificate
                if lastName in listOfCommonCerts:

                    # Check if there was a second word in the first name
                    if len(firstNameRaw.split()) > 1:

                        # Update the last name with the second word in the first name
                        lastName = str(firstNameRaw.split()[1])

                    # Last name is a cert but there was not a second word in the first name
                    else:

                        # Tell the user that the first name was only one word and the word was a title
                        warningMessage += "The last name is a common certificate and there was not a second word in " \
                                          "the first name field. "

                # Check if last name is only an initial "A."
                if len(str(lastNameRaw.split()[0])) == 2 and str(lastNameRaw.split()[0])[-1:] == ".":

                    # Check the email format that the user supplied
                    if emailFormat != "firstl" and emailFormat != "first":

                        # Tell the user that the last name was an initial
                        warningMessage += "The last name is an initial. "

                # Create the combined name
                firstAndLast = firstName + " " + lastName

                # Create the full raw name
                fullNameRaw = firstNameRaw + " " + lastNameRaw

                # Create the email address from the email format
                if emailFormat == "first.last":
                    emailAddress = firstName + "." + lastName + "@" + domainName
                elif emailFormat == "firstlast":
                    emailAddress = firstName + lastName + "@" + domainName
                elif emailFormat == "flast":
                    emailAddress = firstName[:1] + lastName + "@" + domainName
                elif emailFormat == "firstl":
                    emailAddress = firstName + lastName[:1] + "@" + domainName
                elif emailFormat == "lastf":
                    emailAddress = lastName + firstName[:1] + "@" + domainName
                elif emailFormat == "first":
                    emailAddress = firstName + "@" + domainName
                elif emailFormat == "last":
                    emailAddress = lastName + "@" + domainName
                else:
                    emailAddress = ""

                # Print the email address
                print(success + emailAddress)

                # Try to get occupation
                try:
                    occupation = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["miniProfile"]["occupation"])
                except:
                    occupation = ""

                # Try to get profile heading
                try:
                    profileHeading = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["snippets"][0]["heading"]["text"])
                except:
                    profileHeading = ""

                # Try to get location
                try:
                    location = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["location"])
                except:
                    location = ""

                # Try to get industry
                try:
                    industry = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["industry"])
                except:
                    industry = ""

                # Try to get connection
                try:

                    # Check if connection is first
                    if str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["distance"]["value"]) == "DISTANCE_1":

                        # Set connection to first
                        connection = "First"

                    # Check if connection is second
                    elif str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["distance"]["value"]) == "DISTANCE_2":

                        # Set connection to second
                        connection = "Second"

                    # Check if connection is third
                    elif str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["distance"]["value"]) == "DISTANCE_3":

                        # Set connection to third
                        connection = "Third"

                    # Check if connection is out of network
                    elif str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["distance"]["value"]) == "OUT_OF_NETWORK":

                        # Set connection to third
                        connection = "Out of Network"

                    # connection is unavailable
                    else:

                        # Set connection
                        connection = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["distance"]["value"])

                except:
                    connection = ""

                # Try to get premium
                try:

                    # Check if premium is true
                    if str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["premium"]) == "True":

                        # Set premium to true
                        premium = "Yes"

                    # Check if premium is false
                    elif str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["premium"]) == "False":

                        # Set premium to false
                        premium = "No"

                    # Premium is unavailable
                    else:

                        # Set premium
                        premium = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["premium"])

                except:
                    premium = ""

                # Try to get jobSeeker
                try:

                    # Check if jobSeeker is true
                    if str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["jobSeeker"]) == "True":

                        # Set jobSeeker to true
                        jobSeeker = "Yes"

                    # Check if jobSeeker is false
                    elif str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["jobSeeker"]) == "False":

                        # Set jobSeeker to false
                        jobSeeker = "No"

                    # jobSeeker is unavailable
                    else:

                        # Set jobSeeker
                        jobSeeker = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["jobSeeker"])

                except:
                    jobSeeker = ""

                # Try to get influencer
                try:

                    # Check if influencer is true
                    if str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["influencer"]) == "True":

                        # Set influencer to true
                        influencer = "Yes"

                    # Check if influencer is false
                    elif str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["influencer"]) == "False":

                        # Set influencer to false
                        influencer = "No"

                    # Influencer is unavailable
                    else:

                        # Set influencer
                        influencer = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["memberBadges"]["influencer"])

                except:
                    influencer = ""

                # Try to get school name
                try:
                    schoolName = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["educations"][0]["schoolName"])
                except:
                    schoolName = ""

                # Try to get school degree
                try:
                    schoolDegree = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["educations"][0]["degree"])
                except:
                    schoolDegree = ""

                # Try to get school field of study
                try:
                    schoolFieldOfStudy = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["educations"][0]["fieldOfStudy"])
                except:
                    schoolFieldOfStudy = ""

                # Try to get school start year
                try:
                    schoolStartYear = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["educations"][0]["startedOn"]["year"])
                except:
                    schoolStartYear = ""

                # Try to get school end year
                try:
                    schoolEndYear = str(profile["hitInfo"]["com.linkedin.voyager.search.SearchProfile"]["educations"][0]["endedOn"]["year"])
                except:
                    schoolEndYear = ""

            # Profile details not available
            else:

                # Continue looping
                continue

            # Check if there was no search term used
            if keywordsForSearch == "":

                # Add profile details to list
                listOfEmails.append((emailAddress, "www.linkedin.com", warningMessage, "", occupation, profileHeading,
                                     fullNameRaw, firstAndLast, firstName, lastName, publicIdentifier, location,
                                     industry, connection, premium, jobSeeker, influencer, schoolName, schoolDegree,
                                     schoolFieldOfStudy, schoolStartYear, schoolEndYear))

            # A search term was used
            else:

                # Add profile details to list
                listOfEmails.append((emailAddress, "www.linkedin.com", warningMessage, keywordsForSearch, occupation,
                                     profileHeading, fullNameRaw, firstAndLast, firstName, lastName, publicIdentifier,
                                     location, industry, connection, premium, jobSeeker, influencer, schoolName,
                                     schoolDegree, schoolFieldOfStudy, schoolStartYear, schoolEndYear))

            # Update the list of unique identifiers
            listOfPublicIdentifiers.append(publicIdentifier)

            # Determine if you want to update the unique email list. True will remove duplicates when scraping other
            # sites. False allows validation that LinkedIn generated emails were scraped from other websites
            updateUniqueEmailList = False
            
            # Check if the list should be updated
            if updateUniqueEmailList:

                # Update the list of unique email addresses
                listOfUniqueEmails.append(emailAddress)


# Ask the user if they want to continue LinkedIn due to the results being over 1,000
def ask_user_to_continue_generating_emails_from_linkedin():

    # Set a blank error message
    errorMessage = ""

    # Loop until a valid answer has been given
    while True:

        # Ask the user whether they want to continue checking LinkedIn
        continueCheckingLinkedin = input("\n" + errorMessage + "There were over 1,000 profile results. LinkedIn "
                                                               "limited the profiles results to 1,000. Would you like "
                                                               "to continue searching LinkedIn for emails? (y/n)" +
                                                               "\n").lower()

        # Check if the choice is yes
        if continueCheckingLinkedin == "y" or continueCheckingLinkedin == "yes":

            # Return yes
            return True

        # The choice is no
        elif continueCheckingLinkedin == "n" or continueCheckingLinkedin == "no":

            # Return no
            return False

        # Incorrect choice
        else:

            # Set the error message to incorrect choice entered
            errorMessage = failure + "Incorrect choice entered. "


# Get emails from LinkedIn using common search terms
def get_emails_from_linkedin_using_search_terms_that_are_common(numberOfProfilesToDisplayPerPage, emailFormat,
                                                                domainName, companyId, listOfPublicIdentifiers,
                                                                listOfEmails, listOfUniqueEmails, dictOfCookies,
                                                                commonSearchTerms, searchType):

    # Tell the user what is being searched for
    print("\n" + info + "Searching LinkedIn using common " + searchType + ". Press Ctrl+c to stop this search and continue")

    # Try to perform many searches, allowing the user to cancel if needed
    try:

        # Loop through the common search terms
        for searchTerm in commonSearchTerms:

            # Get the number of pages to search
            numberOfLinkedinPagesToSearch = get_the_number_of_linkedin_pages_to_search(numberOfProfilesToDisplayPerPage,
                                                                                       searchTerm, companyId, dictOfCookies)

            # Search for profiles
            search_linkedin_for_profiles(numberOfProfilesToDisplayPerPage, numberOfLinkedinPagesToSearch, searchTerm,
                                         emailFormat, domainName, companyId, listOfPublicIdentifiers, listOfEmails,
                                         listOfUniqueEmails, dictOfCookies)

    # Catch Ctrl+c
    except KeyboardInterrupt:

        # Print that the search stopped
        print("\n" + warning + "Search stopped")

        # Return
        return


# Get emails from LinkedIn
def get_emails_from_linkedin_using_search_terms(numberOfProfilesToDisplayPerPage, emailFormat, domainName, companyId,
                                                listOfPublicIdentifiers, listOfEmails, listOfUniqueEmails,
                                                dictOfCookies):

    # Create a list of common first names
    commonFirstNames = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles", "Joseph",
                        "Thomas", "Kevin", "Jason", "Matt", "Tim", "Larry", "Mary", "Patricia", "Linda", "Barbara",
                        "Elizabeth", "Jennifer", "Maria", "Susan", "Margaret", "Lisa", "Sarah", "Kim", "Jessica",
                        "Melissa", "Amy"]
    
    # Create a list of common last names
    commonLastNames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez",
                       "Wilson"]
    
    # Create a list of common job titles
    commonJobTitles = ["Analyst", "Engineer", "Consultant", "Specialist", "Operator", "Intern", "Associate",
                       "Assistant", "Admin", "Administrator", "Data", "Driver", "Warehouse", "Recruiter", "Tester",
                       "Lead", "Team", "CEO", "COO", "VP", "President", "Director", "Manager", "Operations",
                       "Security", "Audit", "IT", "Information", "Business", "Marketing", "Accounting", "Sales",
                       "Representative", "Project", "Sales"]

    # Create a list of common certifications
    commonCertifications = ["MBA", "PMP", "PHR", "SPHR", "SHRM", "CCNA", "CCNP", "CCIE"]

    # Search LinkedIn using common search terms
    get_emails_from_linkedin_using_search_terms_that_are_common(numberOfProfilesToDisplayPerPage, emailFormat,
                                                                domainName, companyId, listOfPublicIdentifiers,
                                                                listOfEmails, listOfUniqueEmails, dictOfCookies,
                                                                commonFirstNames, "first names")

    get_emails_from_linkedin_using_search_terms_that_are_common(numberOfProfilesToDisplayPerPage, emailFormat,
                                                                domainName, companyId, listOfPublicIdentifiers,
                                                                listOfEmails, listOfUniqueEmails, dictOfCookies,
                                                                commonLastNames, "last names")

    get_emails_from_linkedin_using_search_terms_that_are_common(numberOfProfilesToDisplayPerPage, emailFormat, domainName,
                                                                companyId, listOfPublicIdentifiers, listOfEmails,
                                                                listOfUniqueEmails, dictOfCookies, commonJobTitles,
                                                                "job titles")

    get_emails_from_linkedin_using_search_terms_that_are_common(numberOfProfilesToDisplayPerPage, emailFormat,
                                                                domainName, companyId, listOfPublicIdentifiers,
                                                                listOfEmails, listOfUniqueEmails, dictOfCookies,
                                                                commonCertifications, "certifications")


# Get emails from LinkedIn
def get_emails_from_linkedin(emailFormat, domainName, companyId, listOfPublicIdentifiers,
                             listOfEmails, listOfUniqueEmails, dictOfCookies):

    # Set the number of profiles to display per page to 49 since this is the max allowed
    numberOfProfilesToDisplayPerPage = 49

    # Set a blank search term
    searchTerm = ""

    # Tell the user what is being searched for
    print(info + "Searching LinkedIn. Press Ctrl+c to stop this search and continue")

    # Try to get the number of pages to search for
    try:

        # Get the number of pages to search
        numberOfLinkedinPagesToSearch = get_the_number_of_linkedin_pages_to_search(numberOfProfilesToDisplayPerPage, searchTerm, companyId, dictOfCookies)

    # Catch exception
    except:

        # Return
        return

    # Try to perform the search, allowing the user to cancel if needed
    try:

        # Search for profiles
        search_linkedin_for_profiles(numberOfProfilesToDisplayPerPage, numberOfLinkedinPagesToSearch, searchTerm,
                                     emailFormat, domainName, companyId, listOfPublicIdentifiers, listOfEmails,
                                     listOfUniqueEmails, dictOfCookies)

    # Catch Ctrl+c
    except KeyboardInterrupt:

        # Print that the search stopped
        print("\n" + warning + "Search stopped")

        # Return
        return

    # Check if there were 1,000 results
    if (numberOfProfilesToDisplayPerPage * numberOfLinkedinPagesToSearch) > 999:

        # Ask the user if they want to continue checking LinkedIn
        continueCheckingLinkedin = ask_user_to_continue_generating_emails_from_linkedin()

        # Check if the user wants to continue checking LinkedIn
        if continueCheckingLinkedin:
                
            # Continue checking LinkedIn
            get_emails_from_linkedin_using_search_terms(numberOfProfilesToDisplayPerPage, emailFormat, domainName,
                                                        companyId, listOfPublicIdentifiers, listOfEmails,
                                                        listOfUniqueEmails, dictOfCookies)


# Get emails from www.email-format.com
def get_emails_from_emailformat(domain, listOfEmails, listOfUniqueEmails):

    # Tell the user the search has started
    print("\n" + info + "Searching www.email-format.com for emails.")

    # Get the soup
    soup = get_soup("https://www.email-format.com/d/" + domain)

    # Get all divs
    for div in soup.findAll("div", {"class": "fl"}):

        # Set the email
        email = div.text.strip()

        # Check if the domain is in the email
        if ("@" + domain) in email and "e.g. " not in email:

            # Check if the email is already in the list and not blank
            if email in listOfUniqueEmails:

                # Continue since the profile was already added
                continue

            # Email is not in the list
            else:

                # Print the email
                print(success + email)

                # Add the email to the list
                listOfEmails.append((email, "www.email-format.com"))

                # Add the email to the list of unique email addresses
                listOfUniqueEmails.append(email)


# Get emails from www.skymem.info
def get_emails_from_skymem(domain, listOfEmails, listOfUniqueEmails):

    # Tell the user the search has started
    print("\n" + info + "Searching www.skymem.info for emails. Press Ctrl+c to stop this search and continue")

    # Get the soup
    soup = get_soup("http://www.skymem.info/srch?q=" + domain)

    # Get the link to page 2 results
    for link in soup.findAll("a", href=lambda href: href and "domain" in href):

        # Set the page 2 link
        pageTwoLink = link.get("href")

        # Do not continue searching links
        break

    # Remove the page 2 number
    uniqueToken = pageTwoLink[:-1]

    # Create the full link
    fullLinkWithUniqueToken = "http://www.skymem.info" + uniqueToken

    # Get the soup for page 2 to get the total number of emails
    soup = get_soup(fullLinkWithUniqueToken + "2")

    # Set the initial number of emails to 0
    numberOfEmails = 0
    
    # Get the total number of emails
    for span in soup.findAll("span"):

        # Check if the show first text if found
        if "Show first" in span.text:
            
            # Set the number of emails. span.text == "( Show first XXXX emails. Need more? Use advanced search )"
            numberOfEmails = span.text.split()[3]

            # Do not continue searching
            break

    # Check if no emails were found
    if numberOfEmails == 0:

        # Tell the user that no emails were found
        print(warning + "No emails found at www.skymem.info")

        # Return
        return

    # Round up to the nearest page. There are 20 emails per page.
    numberOfPages = int(math.ceil(float(numberOfEmails) / 20))

    # Loop through all the page numbers
    for pageNumber in range(1, numberOfPages + 1):

        # Print the page number
        print("\n" + info + "Searching www.skymem.info page " + str(pageNumber) + " of " + str(numberOfPages))

        # Set the url to open
        url = fullLinkWithUniqueToken + str(pageNumber)

        # Get the soup
        soup = get_soup(url)

        # Get the emails on the page
        for email in soup.findAll("a", href=lambda href: href and ("@" + domain) in href):

            # Check if the email is already in the list and not blank
            if email in listOfUniqueEmails:

                # Continue since the profile was already added
                continue

            # Email is not in the list
            else:

                # Print the email
                print(success + email.text)

                # Add the email to the list
                listOfEmails.append((email.text, "www.skymem.info"))

                # Add the email to the list of unique email addresses
                listOfUniqueEmails.append(email.text)


# Save the list of emails
def save_emails(filename, listOfEmails):

    # Check that there are emails to save
    if len(listOfEmails) > 1:

        # Save the results as a csv file
        with open(filename, "wb") as fileOfEmails:
            csvWriter = csv.writer(fileOfEmails, quoting=csv.QUOTE_ALL)
            csvWriter.writerows(listOfEmails)

        # Tell the user the file has been saved
        print("\n" + info + "Results have been saved to " + filename)

    # No emails found
    else:

        # Tell the user that there were no matches
        print("\n" + warning + "No results found")


# Main
def main():

    # Print the banner
    print_banner()

    # Create a list with column headers to store the emails
    listOfEmailAddresses = []
    listOfEmailAddresses.append(("Email Address", "Source", "Warning Message", "Search Term", "Occupation",
                                 "Profile Heading", "Full Name", "First & Last", "First Name", "Last Name",
                                 "Identifier", "Location", "Industry", "Connection", "Premium", "Job Seeker",
                                 "Influencer", "School", "Degree", "Field of Study", "School Start", "School End"))

    # Create a list to store only the email addresses
    listOfUniqueEmailAddresses = []
    
    # Create a list of unique identifiers to avoid adding duplicate profiles from LinkedIn
    listOfLinkedinPublicIdentifiers = []
    
    # Ask the user for the domain
    domain = ask_user_for_domain()

    # Ask the user for the output filename
    outputFilename = ask_user_for_output_filename(domain)

    # Check if the file is open
    check_outputfile(outputFilename, listOfEmailAddresses)

    # Ask the user for the email format
    emailFormat = ask_user_for_email_format(domain)

    # Ask the user if they want to check LinkedIn for emails
    checkLinkedin = ask_user_to_generate_emails_from_linkedin()

    # Check if the user wants to check LinkedIn for emails
    if checkLinkedin:

        # Ask the user for their LinkedIn email
        linkedinEmail = ask_user_for_linkedin_email()
        
        # Ask the user for their LinkedIn password
        linkedinPassword = ask_user_for_linkedin_password()

        # Log the user into LinkedIn
        dictionaryOfCookies = login_to_linkedin(linkedinEmail, linkedinPassword)

        # Check if the login was not successful
        if dictionaryOfCookies == None:

            # Tell the user that the login was not successful
            print(warning + "Unable to login to LinkedIn. Trying again" + "\n")

            # Log the user into LinkedIn
            dictionaryOfCookies = login_to_linkedin(linkedinEmail, linkedinPassword)
        
        # Check if the login was not successful
        if dictionaryOfCookies == None:

            # Tell the user that the login was not successful
            print(warning + "Unable to login to LinkedIn" + "\n")

        # Login was successful
        else:
            
            # Ask the user for the company ID
            companyId = ask_user_for_linkedin_company_id(dictionaryOfCookies)

            # Generate emails from LinkedIn data
            get_emails_from_linkedin(emailFormat, domain, companyId, listOfLinkedinPublicIdentifiers,
                                     listOfEmailAddresses, listOfUniqueEmailAddresses, dictionaryOfCookies)

    # Try to scrape emails
    try:

        # Get emails from emailformat
        get_emails_from_emailformat(domain, listOfEmailAddresses, listOfUniqueEmailAddresses)

    # Catch Ctrl+c
    except KeyboardInterrupt:

        # Print that the search stopped
        print("\n" + warning + "Search stopped for www.email-format.com")

    # Error getting emails
    except:

        # Tell the user that emails were not found
        print(warning + "An issue occured while scraping emails from www.email-format.com")

    # Try to scrape emails
    try:

        # Get emails from skymem
        get_emails_from_skymem(domain, listOfEmailAddresses, listOfUniqueEmailAddresses)

    # Catch Ctrl+c
    except KeyboardInterrupt:

        # Print that the search stopped
        print("\n" + warning + "Search stopped for www.skymem.info")

    # Error getting emails
    except:

        # Tell the user that emails were not found
        print("\n" + warning + "An issue occured while scraping emails from www.skymem.info")

    # Save the list of emails
    save_emails(outputFilename, listOfEmailAddresses)


# Only execute when running as primary module or called from another script
if __name__ == "__main__":

    # Execute main, get status code
    status = main()

    # Terminate with status code from main
    sys.exit(status)
