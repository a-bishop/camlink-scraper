## Camlink Timetable Scraper

### Description

Uses the Selenium library with Beautiful Soup, to log in and scrape Camosun student timetable information by term and export the data to a CSV file, or optionally a JSON file, for use elsewhere. An example of how the data can be used is [hosted here](https://github.com/a-bishop/react-view-timetable).

### Instructions

#### 1) Download Chrome WebDriver

&nbsp;&nbsp;Mac (via homebrew):  ```brew install chromedriver```

&nbsp;&nbsp;Windows: [ChromeDriver download site](http://chromedriver.chromium.org/downloads) (place .exe file in C:\Windows folder)

#### 2) Install Dependencies

#### Selenium
```[python3 -m] pip install selenium```

#### Beautiful Soup

```[python3 -m] pip install beautifulsoup4```

### Usage

```python[3] scrape_camlink.py [-v] [-json]```

Prompts for Camlink username, password and the school term to search for (ex. 2019W). Exports a CSV file to the current directory, named "camosunCourses[schoolterm].csv".

```-v``` is the verbose flag, will cause the program print out more info about what's happening as it runs.

If the ```-json``` flag is set, the program will additionally output a document with the same name into the current directory in json format.



