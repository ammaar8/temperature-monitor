[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ammaar8/temperature-monitor">
    <img src="images/logo.png" alt="Logo" height="80">
  </a>

  <h3 align="center">Temperature Monitor</h3>

  <p align="center">
    An indoor temperature and humidity monitoring project.
    <br />
    <br />
    <br />
    <a href="https://temperature-monitor.herokuapp.com/">View App</a>
    ·
    <a href="https://youtu.be/yWvnplurRp4">Demo Video</a>
    ·    
    <a href="https://github.com/ammaar8/temperature-monitor/issues">Report Bug</a>
    ·
    <a href="https://github.com/ammaar8/temperature-monitor/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->                                          
<details open="open">
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
        <li><a href="#schematic">Schematic</a></li>
        <li><a href="#arduino">Arduino</a></li>
        <li><a href="#app">App</a></li>
        <li><a href="#logger">Logger</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
        <ul>
            <li><a href="#logging">Logging</a></li>
            <li><a href="#deploying">Deploying</a></li>
        </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot](images/showcase.png)
This is a hobby project in which sensor data is being published to a heroku database and can be visualized using a dash web app. This project can be repurposed to visualize any type of numeric data from sensors.


### Built With

* [Dash](https://plotly.com/dash/)
* [Heroku](https://heroku.com)
* [Arduino](https://www.arduino.cc/)
* [Pandas](https://pandas.pydata.org/)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
To get started with this project you will need:
1. Arduino UNO
2. DHT11 Sensor

### Install
1. Install python requirements
```
pip3 install -r requirements.txt
```
2. Install [Heroku](https://devcenter.heroku.com/articles/heroku-cli)

<!-- SCHEMATIC -->
### Schematic
Build the circuit according to the schematic.
![Image](images/schematic.png)

<!-- ARDUINO -->
### Arduino
After completing the hardware part upload [temperature_monitor.ino](arduino/temperature_monitor.ino) to the arduino.

<!-- App -->
### App
First we need to create a heroku app. Ensure you have installed heroku by running `heroku -v`. To create an app follow these steps:
1. Login to heroku.
```
heroku login
```
2. Create a heroku app.
```
heroku create app-name
```
3. Once the app is created, we have to add the [Heroku Postgresql add-on](https://devcenter.heroku.com/articles/heroku-postgresql).
```
heroku addons:create heroku-postgresql:hobby-dev
```
4. After adding the add-on, we have to create a table on the app database.
```
heroku pg:psql -a app-name
```
```
CREATE TABLE dht_data (
  created_on serial not null,
  logged_on timestamptz not null,
  temperature numeric(4,2) not null,
  humidity numeric(4,2) not null,
);
```
This wil create a table named 'dht_data' with columns created_on, logged_on, temperature and humidity. We can now push data to our database from our temperature logger script.

<!-- Logger -->
### Logger
To setup the logger to push data to our database reate a database.ini file with the database details in the `logger` folder.
```
[postgresql]
database=
host=
port=
user=
password=
sslmode=require
```
You can get the details by running `heroku pg:credentials:url -a your-app-name.`

<!-- USAGE EXAMPLES -->
## Usage

<!-- LOGGING DATA -->
### Logging
To log sensor data:
1. Check the `DEVICE_PATH` is set correcly in `temperature_logger.py`
2. Run `python3 temperature_logger.py`

<!-- DEPLOYING TO HEROKU -->
### Deploying
We are only deploying the App folder of the project on Heorku. To do this, we make use of the subtree command in git. Run this to push the App to heroku
```
git subtree --prefix App push heroku main
```
Once the app is deployed, it will print a url like http://temperature-monitor.herokuapp.com which you can visit to view the app. 

### Running Locally
Running locally is required to test changes before deploying the app. Here is how to do it.
1. `cd` to `App` folder and copy Heroku config vars to local .env file.
```
heroku config:get DATABASE_URL -s  >> .env
```
2. Run the app.
```
heroku local
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Ammaar Solkar - asketch8@gmail.com

Project Link: [https://github.com/ammaar8/temperature-monitor](https://github.com/ammaar8/temperature-monitor)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Readme Template](https://github.com/othneildrew/Best-README-Template/)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ammaar-solkar
