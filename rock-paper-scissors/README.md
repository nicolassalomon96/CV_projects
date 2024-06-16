<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth">
    <img src="images/game_logo.png" alt="Logo" width="240" height="120">
  </a>

<h3 align="center">An AI hand-controlled labyrinth game</h3>

  <p align="center">
    A game that uses your hand to control your movements in order to pass a labyrinth.
    <br />
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth/outputs/output_score_gif.gif">View Demo</a>
    ·
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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

I present you an innovative game that uses computer vision technology to recognize the player's hand through a webcam. This advanced system allows you to control a virtual joystick to navigate a maze on the screen, offering an intuitive and accessible gaming experience. By employing AI techniques such as hand detection and tracking, image segmentation, and gesture recognition, this game redefines interaction in the gaming world, providing total immersion and a unique way to play. Discover the future of video games with this revolutionary application and enjoy your time playing!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][Python]][Python-url]
* [![NumPy][NumPy]][NumPy-url]
* [![Pytorch][Pytorch]][Pytorch-url]
* [![MediaPipe][MediaPipe]][MediaPipe-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may set up this project locally in your computer.
To get a local copy up and running follow these simple example steps.

### Prerequisites

The following packages may be installed in order to run the code:

* Numpy
  ```sh
  pip install numpy
  ```
* OpenCV
  ```sh
  pip install opencv-python
  ```
* Mediapipe
  ```sh
  pip install mediapipe
  ```
* Matplotlib
  ```sh
  pip install matplotlib
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth
   ```
2. Install required packages listed on Prerequisites

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

If you want to play, just run _mediapipe_hand_labyrinth.py_
```sh
python mediapipe_hand_labyrinth.py
```
Once you pass your finger through the **START**, the score will begin to run. Avoid touching borders of the labyrinth because you'll loose. Good Luck! 

This project is based on Google Mediapile Framework, through it we can get our finger position. A more detailed description is given below:

* After initializing the webcam video capture, the hand keypoint detector is instantiated. It will be responsible of detecting your finger using the Mediapipe Framework 
```sh
detector = LandmarkDetector()
```

* A PNG image of the labyrinth is loaded and resized. Variables are initialized to track the state of the game, the position of the fingertip, a mask for drawing the path of the finger, and the start and current times.

* Once the labyrinth and the masks necessary to detect a crossing along the border lines are loaded, the key points of the left hand are detected in the image.
```sh
left_det, left_detections_list = detector.get_positions(image, kind='left_hand', draw=False) #for detect left hand fingertip
```

* It is checked if the tip of the finger has passed the start line. If so, the start is marked, the path of the finger is drawn and the time is recorded. If the tip of the finger has passed the finish line, the end is marked and the time is shown.

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

Project Link: [https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth](https://github.com/nicolassalomon96/CV_projects/tree/main/mediapipe_hand_labyrinth)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/output_example.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[OpenCV]: https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white
[OpenCV-url]: https://opencv.org/
[Pytorch]: https://img.shields.io/badge/PyTorch-black?logo=PyTorch
[Pytorch-url]: https://pytorch.org/
[Ultralytics]: https://img.shields.io/badge/ultralytics-v8.1.0-blue
[Ultralytics-url]: https://docs.ultralytics.com/
[NumPy]: https://img.shields.io/badge/-NumPy-013243?style=flat&logo=numpy&logoColor=white
[NumPy-url]: https://opencv.org/
[MediaPipe]: images/mediapipe_logo.png
[MediaPipe-url]: https://mediapipe-studio.webapps.google.com/home