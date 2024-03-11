![image](https://github.com/mizaqq/Basic_stock_analysis/assets/59586131/313a6eab-2ca2-47b6-b236-d1e06ef160a4)<a name="readme-top"></a>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The Django Stock Analysis Project is a web application built using the Django framework, designed for basic stock analysis. 
It provides users with a user-friendly interface to analyze stock data, view historical trends, and make informed investment decisions.
The project leverages Django's powerful features to manage user authentication, handle database operations, and deliver dynamic content.
Site also allows to scrap companies data using REST API
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python
* Django
* Bootstrap
* Docker
Developed using AWS

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

* Docker 

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Turn on docker
2. Login to docker
3. docker run -e DJANGO_ALLOWED_HOSTS=* -p 8000:8000 mizaqq/basic_django_proj_run2
Use -e flag to set up enviroment variables. Api Secret keys for scrapping data are also to be set up like this. All the endpoints are free-to-use.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Already existing companies are listed on the main page.
![image](https://github.com/mizaqq/Basic_stock_analysis/assets/59586131/6151dda6-15d5-4e1f-8b8b-eb7fd5ca0920)

You can add your own company to get its data to be analyzed if it is not already in database by giving its name and stock symbol
![image](https://github.com/mizaqq/Basic_stock_analysis/assets/59586131/6e1322ff-b6ec-421f-9083-8802f607de2d)

Get all the companies data and its basic indexes.
![image](https://github.com/mizaqq/Basic_stock_analysis/assets/59586131/f0c57c11-7dea-4233-bd63-1c21c02ca2d5)

Scrap companies data using api endpoint 
Link http://16.171.170.50:8000/api/
You can get your own api key by logging in and going to your account details. You can also regenerate your token there

Authentication has to be passed by Header in format "Authentication: Token <YOUR-API-KEY>

Python example
```
url = 'http://127.0.0.1:8000/api/'
headers = {'Authorization':'Token <YOUR-API-KEY'}
response = requests.get(url, headers=headers)
data = response.json()
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>




Project Link: [https://github.com/your_username/repo_name](https://github.com/mizaqq/basic_stock_analysis)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>


