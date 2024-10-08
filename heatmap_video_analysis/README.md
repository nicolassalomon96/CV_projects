<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app">
    <img src="images/Readme/logo.png" alt="Logo" width="100" height="100">
  </a>

<h3 align="center">Face Attendance App using Mediapipe and Face Recognition</h3>

  <p align="center">
    Useful Face Attendance App using Mediapipe to extract facial mesh and identify each user. It allows you to create a user with a name, username, and password, and records each registration with the name and datetime.
    <br />
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app/images/Readme/output_test.png">View Demo</a>
    ·
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
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
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

* Project Summary and Importance

This project utilizes Mediapipe to capture the facial mesh of a person through a webcam and generate a unique user and password for each individual in a registration application. This innovative computer vision solution offers numerous applications and advantages across various fields.

* Applications

1. Attendance Control: Perfect for schools, universities, and offices where automatic attendance recording can save time and increase accuracy.
2. Secure Access: Ideal for access control systems in buildings and events, providing a secure and contactless way to verify identity.
3. Client Monitoring: In gyms and wellness centers, it enables efficient tracking of facility usage and client preferences.
4. Hospitality: In hotels and restaurants, it facilitates quick and efficient guest registration and management.

* Advantages

1. Accuracy and Efficiency: Mediapipe technology ensures high precision in facial recognition, minimizing errors and saving time.
2. Ease of Use: With a user-friendly interface and the ability to use a standard webcam, the application is accessible to any user.
3. Enhanced Security: By generating unique users and passwords based on facial features, system security is enhanced, reducing the risk of identity fraud.
4. Versatility: Applicable in multiple industries and scenarios, from education and healthcare to security and entertainment.
5. Automation: Reduces the need for manual intervention, freeing up human resources for more critical tasks and improving operational efficiency.

* Conclusions

In summary, this project represents a significant advancement in the integration of computer vision technologies for practical, everyday applications, providing innovative and effective solutions for person registration and management.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][Python]][Python-url]
* [![OpenCV][OpenCV]][OpenCV-url]
* [![NumPy][NumPy]][NumPy-url]
* [![MediaPipe][MediaPipe]][MediaPipe-url]
* [![Tkinter][Tkinter]][Tkinter-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may set up this project locally in your computer.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Install the packages listed on requirements.txt:
  ```sh
  pip install -r requirements.txt
  ```

If you have problems with face_recognition package, please try:
  ```sh
  conda install -c conda-forge dlib
  pip install cmake
  pip install face_recognition
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app
   ```
2. Install required packages listed on Prerequisites

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

In order to probe or use this project you must run main.py script:
```sh
  python main.py
```

First of all you need to create or register an user:

* Write your desire name, username and password.
* Click the register button and wait for the Biometric Registration Window.
* Stay looking at the camera and blink twice. If you take your view off the camera, the blink count will reset for security.
* Wait for the success confirmation window.

In order to Log In:

* Click on the Log In button and wait for the Biometric Login Window.
* Stay looking at the camera and blink twice. If you take your view off the camera, the blink count will reset for security.
* If the face was recognized, a Profile Window will display the user's photo, name and username.

<div align="center">
  <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app/images/Readme/output_test.png">
    <img src="images/Readme/output_test.png" alt="Logo" width="1286" height="350">
  </a>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
<!--
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

<!-- CONTRIBUTING -->
<!--
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- LICENSE -->
<!--
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


<!-- CONTACT -->
## Contact
Any comment or contribution is welcome and I will be attentive to respond to you :)

Nicolás Salomón - [Linkedin](https://www.linkedin.com/in/nicolassalomon96/) - [Gmail](nicolassalomon96@gmail.com)

Project Link: [https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app](https://github.com/nicolassalomon96/CV_projects/tree/main/face_attendance_app)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/Readme/output_test_1.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[OpenCV]: https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white
[OpenCV-url]: https://opencv.org/
[NumPy]: https://img.shields.io/badge/-NumPy-013243?style=flat&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
[MediaPipe]: images/Readme/mediapipe_logo.png
[MediaPipe-url]: https://mediapipe-studio.webapps.google.com/home
[Tkinter]: https://img.shields.io/badge/Made_with-tkinter-blue?style=for-the-badge
[Tkinter-url]: https://docs.python.org/es/3/library/tkinter.html