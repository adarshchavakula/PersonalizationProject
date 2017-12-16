# Last.fm Recommender System

We chose to investigate the Last.fm data set using a temporal collaborative filtering model.  Specifically, we want to investigate the effect that time of day and weekday has on the users' listening habits.  Our objective is to reduce the number of times a user will skip the song.  Because we are using skips as a proxy for a users' enjoyment of the song, we do not need to rely on explicit feedback, such as the users' song ratings.  In addition, since consumer preferences change over time, we do not account for how long it has been since a user has rated a song.  Skips occur in the present so we can ignore this recency factor.

## The Data

Last.fm data set contains:
* Listening habits for 992 users
* 173,921 artists with timestamped entries
* Metafile containing user profiles (e.g., gender, age, country and signup date).

The dataset can be found through this [link](http://www.dtic.upf.edu/~ocelma/MusicRecommendationDataset/lastfm-1K.html). The data was collected by Òscar Celma.
 
The dataset records users’ listening history without recording explicit feedback on artist and track pairs.  As there is no input from a user on whether they liked or disliked a track, we initially treat the data as an indication of positive preference. This will be expanded to include skips for the full recommender system.

A preview of the data is shown here, with the leftmost column as the Pandas index:
![Data Preview](data/DataPreview.png)

The following is the play counts for the entire data set, grouped by hour of the day (left) and day of the week (right):
![Play Counts by hour of day and day of week](data/PlayCounts.png)

## Part I

### Objective
We were interested in learning how neighborhood- and model-based collaborative filtering (CF) algorithms perform on aggregated data. These CF approaches help us understand how an improved recommendation engine can drive increased user engagement within a music platform.  We then utilized timestamps for the final project along with other metadata to improve the quality of our recommendations.

### Models: Neighborhood Collaborative Filtering and SVD
We implemented a neighborhood based collaorative filtering technique for our user-based CF and implemented the SVD algorithm as our model-based CF. With these two models we predicted values indicating whether a user would listen to a particular artist. For more information, please read [Part I Detailed Analysis](Part I Detailed Analysis.md).

### Conclusion
The neighborhood-based collaborative filter results in a better RMSE at higher values of K, but does not bring MAE to a competitive level when compared to the baseline model. On the other hand, the SVD model-based collaborative filter outperforms the baseline at almost every comparison. Our results suggest that the SVD model would be more effective at predicting user preferences. We believe this model would be helpful for a draft recommender system.

## Part II

### Objective

We incorporated `timestamp` to further clarify users’ preferences for artists and tracks.  Based on these data points, we have derived a skips parameter. This parameter indicates whether the user skipped a song (i.e. clicked next in the Last.fm platform). The information from predicted skip values could help us answer questions such as:

* Can music recommendation be improved by incorporating skips?
* Can we use timestamps and skips to identify the user’s mood in a given time period (i.e., genre preference given a certain time of day)?
* After how many times of listening to a track is a user more likely to start skipping the track?

### Model: Neural Network and SVD++ Ensemble
We used a hybrid approach, combing a neural network and a temporal SVD++ model.  The neural network incorporates recency into the model, identifying how user preferences shift over the duration of their listening history. The SVD++  model incorporates periodicity, identifying whether a user is listening to a song during the week or over the weekend. The SVD++ model also brings in a collaborative filtering component, identifying similarities between user-song pairs in the latent space to predict probability of skipping a song a user has not listened to before. We created the ensemble through a linear combination of these two models, with 90% SVD++ and 10% Neural Network. For more information, please read [Part II Detailed  Analysis](Part II Detailed Analysis.md).

### Conclusion
The neural network trains in a matter of minutes with a multitude of features, while the SVD++ model required several hours to train with only two features. Nevertheless, our SVD++ model significantly outpeformed the neural network. As a result, we weighted the SVD model as 90% of our combined linear ensemble and gave 10% weights to the neural network. The AUC from the ensemble, **0.812**, is marginally higher than the SVD++ model alone AUC, **0.807**. The ensemble is significantly higher than the neural network AUC, **0.679**. The benchmark AUC is **0.759**, obtained using the percentage of song-skips per user. An AUC of 0.81 suggests that the ensemble model beats the benchmark and we can leverage it for music recommendations in a commercial setting. 
