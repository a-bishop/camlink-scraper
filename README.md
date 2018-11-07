## Camlink Timetable Scraper

### Description

Uses the Selenium library with Beautiful Soup, to login and scrape Camosun student timetable information by term and export the data to a CSV file for use elsewhere.

### Dependencies

#### Chrome Webdriver

Mac (via homebrew):  
```brew install chromedriver```

Windows:  
[ChromeDriver download site](http://chromedriver.chromium.org/downloads)  
(place .exe file in C:\Windows folder)

#### Selenium

```[python 3 -m] pip install selenium```

#### Beautiful Soup

```[python 3 -m] pip install beautifulsoup4```

### Usage

```python[3] scrape_camlink.py [-v]```

(```-v``` is the verbose flag, will cause the program print out more info about what's happening as it runs.)

Prompts for Camlink username, password and the school term to search for (ex. 2019W). Exports a CSV file to the current directory, named "camosunCourses[schoolterm].csv".





