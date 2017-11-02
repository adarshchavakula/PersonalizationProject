# Last.fm Recommender System

We chose to investigate the Last.fm data using a temporal collaborative filtering model; specifically, we want to investigate the effect time of day and day of the week has on users' listening habits, with our objective to reduce the number of times a user will skip the song. Because we are using skips as a proxy for a user's enjoyment of the song, we do not need to rely on explicit feedback data, such as a user's song rating. In addition, we do not need to be wary of how long it has been since a user has rated a song, since consumer preferences can change over time. Because skips are all in the present, we can ignore this recency factor.

## The Data

Last.fm dataset contains:
* Listening habits for roughly 992 users
* 173,921 artists with timestamped entries
* Metafile containing user profiles (e.g., gender, age, country and signup date).
 
The dataset records users’ listening history without recording explicit feedback on artist and track pairs.  As there is no input from a user on whether they liked or disliked a track, we initially treat the data as an indication of positive preference. This will be expanded to include skips for the full recommender system.

A preview of the data is shown here, with the leftmost column as the Pandas index:
![Data Preview](data/DataPreview.png)

The following is the play counts for the entire dataset, grouped by hour of the day (left) and day of the week (right):
![Play Counts by hour of day and day of week](data/PlayCounts.png)

## Part I Objective
We are interested in learning how neighborhood- and model-based collaborative filters (CF) compare against each other in terms of AUC and RMSE.  These CF approaches will help us understand how an improved recommendation engine can drive increased user engagement with the music platform.  In addition, a good implementation of a CF engine has potential to reduce royalties paid by the platform by minimizing skips (see Part II Objective) and suggesting tracks that users are more likely to enjoy.

We are using the **insert name** as a benchmark for a neighborhood-based CF because **insert reason**.
* How was the data preprocessed?
* What similarity metric did you use?
* How are the training, tuning and test datasets defined?
* How is the model evaluated?

We are using the **insert name** as a benchmark for a model-based CF because **insert reason**.
* How was the data preprocessed?
* How are the training, tuning and test datasets defined?
* How is the model evaluated?

### Table 1. Model Comparison
Model | AUC | RMSE | Metric 3
--- | --- | --- | ---
Neighborhood-Based | XXX | XXX | XXX
Model-Based | XXX | XXX | XXX


## Part II Objective
We will incorporate timestamps and signup dates to further clarify users’ preferences for artists and tracks.  Based on these data points, we can derive a skips parameter.  This parameter indicates whether the user skipped to the next track in the playlist and will help us answer questions such as:
* Can skips be used to improve music recommendation?
* Can we use timestamps and skips to identify the user’s mood (i.e., genre preference given an unspecified activity)?
* After how many times of listening to a track is a user more likely to start skipping the track?
 
 
## Sources/Relevant Literature
 
Hu, Y., Koren, Y., & Volinsky, C. Collaborative Filtering for Implicit Feedback Datasets. Retrieved from http://yifanhu.net/PUB/cf.pdf
