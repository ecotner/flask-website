# Data science
As a data scientist, my job is to take data, clean it, analyze it, and use it to generate recommendations, forecasts, or other actionable insights that other people can use. I do NOT just make pretty plots, reports and dashboards all day though. You can divide analytics into three disciplines: **descriptive**, **predictive**, and **prescriptive**. Descriptive analytics is analyzing what happened in the past, and using that to create plots/reports/dashboards. Predictive analytics is using past data to try and (a) predict what will happen in the future, or (b) infer some information from incomplete knowledge (like "I predict that this image is a picture of a cat"). Prescriptive analytics builds off the results of descriptive and predictive analytics efforts to use the data that we have now to suggest the optimal course of action to take in order to induce the best outcome.

My professional work involves a tiny bit of descriptive (have to have *some* plots to show during meetings), but mostly predictive and prescriptive analytics. I have used statistical and machine learning methods to do things such as forecast which customers will order in the coming days, what delivery routes will look like tomorrow, determine the optimal sequence of orders to deliver, suggest optimal days to schedule inbound vendor deliveries, and cluster similar products to improve our demand forecast accuracy. As you can see, the general theme of my work is in supply chain operations, and involves a good deal of operations research, which I enjoy very much, because the mathematical tools used are significantly different from those I used to use as a physicist, so I get to learn new things all the time.

# Machine learning
Part of a data scientist's job is being able to use machine learning to extract insights from data. In a nutshell, machine learning is a set of techniques for getting a computer to complete tasks without telling it explicitly what to do. While there is immense practical value in using ML methods to solve business problems, I am also incredibly interested in it from a mathematical perspective. There is a lot of beautiful theory that goes into making these algorithms that a lot of practitioners ignore because either it is too difficult to understand, or someone has made a `scikit-learn` estimator that turns it into a black box so you don't *need* to understand to get the job done.

Below is a sample of some of the machine-learning projects that I have worked on. If it's something I've done for fun or my own personal study, I'll have a link to the project. If not, it's probably something I've done for my employer, and I don't think they'd appreciate if I shared proprietary code.

## Supervised
Supervised learning describes algorithms that learn tasks by example. You show a machine how something should be done, and it will try to learn a way to minimize the error between the way it does things, and the "right way" to do things. This can include classification, regression, and forecasting. A simple mathematical way of looking at it is that if you have a ground truth answer $y$ which is determined by some data $x$, a supervised learning algorithm tries to learn the function $f(x;\theta) \approx y$, where $\theta$ are the parameters of the algorithm.

* [Spam classification in text messages](https://nbviewer.jupyter.org/github/ecotner/MachineLearningAlgorithms/blob/master/Supervised/Classification/SpamClassifier/SpamClassification.ipynb)
    - Used natural language processing to classify text messages as either spam or "ham" (i.e. not spam) using a variety of ML techniques. Analyzed risk/reward trade-off of false positives/negatives.
* [CO2 level forecasting](https://github.com/ecotner/MachineLearningAlgorithms/blob/master/Supervised/TimeSeries/CO2_Concentrations/CO2_Concentration.ipynb)
    - Used data from the Mauna Loa observatory in Hawaii in order to forecast $CO_2$ concentration levels and investigate periodicity. Big surprise - global warming is causing $CO_2$ to increase rapidly, and unfortunately the rate is increasing.
* [Pixel-wise classification of microscopy images](https://github.com/ecotner/Kaggle/tree/master/NucleusSegmentation)
    - Part of the 2017 Kaggle Data Science Bowl. The goal was to perform image segmentation by overlaying a mask on top of cellular nuclei to help researchers interpret the images in order to speed up biomedical research. I used a special type of convolutional neural network called a "U-Net" which is able to make accurate predictions at the pixel level.

<center><img src="static/media/nucleus_segmentation.png" width="500px"></center>
    
* [Handwritten digit classification](https://github.com/ecotner/Kaggle/tree/master/DigitRecognizer)
    - Used a Residual Network (ResNet) to classify handwritten digits from the MNIST database.
* [Iris classification](https://nbviewer.jupyter.org/github/ecotner/MachineLearningAlgorithms/blob/master/Supervised/Classification/Iris/IrisClassification.ipynb) and [Titanic survivor prediction](https://github.com/ecotner/Kaggle/tree/master/Titanic)
    - Two exercises that are well-suited to simple classification algorithms. Basically the "hello world" of machine learning.

## Unsupervised
Unsupervised learning describes algorithms that can extract patterns from data without being told explicitly what to do. This includes clustering (like what's pictured in the banner image at the top of the page), dimensional reduction, autoencoders, etc. The set of tasks that unsupervised learning can solve are much more varied, though less well-defined than those of supervised methods, since there is no known "right answer".

* Product demand time series clustering
    - At ATD, our forecasting software takes in a set of "seasonality groups", which are clusters of products that have similar seasonal demand patterns. Before I started there, this process was done manually; after applying unsupervised clustering techniques, I was able to both automate the process and improve the clusters significantly.
* [Convolutional autoencoder (CAE)](https://github.com/ecotner/MachineLearningAlgorithms/tree/master/Unsupervised/Autoencoders/ConvolutionalAutoencoder)
    - Used a convolutional neural network to compress and reconstruct images of handwritten digits from the MNIST database.

## Reinforcement learning
Reinforcement learning is a more general paradigm where a machine learns to complete a task through trial and error. Unlike supervised learning, where there is a "correct" answer the algorithm tries to achieve given an input, a reinforcement learning agent (1) tries to maximize a "reward" which is given for accomplishing a task, and (2) learns an optimal *sequence* of actions rather than just a single prediction. This branch of machine learning is based on a statistical framework for optimizing sequential decisions called *Markov Decision Processes* (MDP).

* Determining optimal delivery times for customers with flexible delivery dates
    - A project I'm currently working on for ATD; we have a set of customers who are flexible about the day they receive their orders on, and it may not be cost effective to deliver to a customer unless there are other customers nearby. So I devised an algorithm that uses MDP's to calculate the expected value of delaying the decision to ship the order, then compares with the current estimate to ship, and chooses the lowest-cost action.
* [Sutton & Barto exercises](https://github.com/ecotner/MachineLearningAlgorithms/tree/master/ReinforcementLearning/RLExercises)
    - While teaching myself the foundations of reinforcement learning, I studied from and completed exercises from [this excellent textbook](http://incompleteideas.net/book/the-book.html).
* [Learning to play Pong](https://github.com/ecotner/MachineLearningAlgorithms/blob/master/ReinforcementLearning/Q-learning/Pong/README.md)
    - Trained a reinforcement learning agent to play the game of Pong using a Deep Q-Network (it honestly wasn't that deep), using nothing but the raw pixels from the game screen as input. After 6 days of training on a GPU (2500 simulated games, 3.5 million frames), the RL agent (green, right) finally was able to outperform the built-in, pre-programmed opponent (orange, left).

<center><img src="static/media/pong_animation.gif" width="300px"></center>

## Other
I've done some other minor machine learning work, like playing around with various neural network architectures, writing my own optimization algorithms, etc. These are all either works in progress, things that didn't work but were still interesting, and other miscellaneous things.

* [Inception ResNet implementation](https://github.com/ecotner/MachineLearningAlgorithms/blob/master/Architectures/ResNet.py)
    - Standalone script for generating ResNets with Inception blocks with TensorFlow (probably outdated since the release of TF 2.0)
* [Deep learning presentation for statistics class](https://www.dropbox.com/s/3hoili685p4ynfb/DeepLearningPresentation.pdf?raw=1)
* [Deep Convexity Annealing](https://github.com/ecotner/ConvexityAnnealing)
    - Experimental optimization algorithm that uses ideas from [graduated optimization](https://en.wikipedia.org/wiki/Graduated_optimization) to train neural networks
* [Multidimensional Bisection](https://github.com/ecotner/MachineLearningAlgorithms/tree/master/Optimization/MultidimensionalBisection)
