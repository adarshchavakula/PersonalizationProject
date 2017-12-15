# Final Project

## Introduction
We designed a recommender system that predicts a user's probability of skipping a song. We created a `skipped` parameter that identifies whether a user skipped the song. Specifically, if a user listens to a song for less than sixty seconds, we consider that to be a skip.

In our review of various recommendation engines that are based on users’ listening habits, we have not encountered an approach that modeled the users’ skip preferences. We believe this parameter adds significant value as it helps us understand the users’ preference for a song based on implicit data. It may be that the user has grown tired of the song and no longer wants to hear it, but it can also be the case that the user is in a different listening mood and prefers to listen to something else. This has been the primary motivation for incorporating skips.

### Approach
We chose to build a hybrid model using a neural network and SVD++.

The neural network incorporates recency into the model, identifying how user preferences shift over the duration of their listening history. Additionally, the neural network identifies latent features that affect the users' decision to skip a song.

Our SVD++ model incorporates periodicity. It also incorporates songs that the user has not yet heard, or songs in a new period, by identifying similarities in the latent space. We modified our ratings matrix to include skips and to incorporate a period for each song: whether or not it was the weekend. The SVD++ approach is a more complex version of the SVD baseline model from Part I. The model adds an implicit user-factor matrix to adjust the explicit user-factor matrix.

Since both models output a vector of the probability a user will skip a song, we chose to run the models independently and combine the probabilities afterwards, hoping that the combined probability would improve the model's accuracy.

### Data
We continued to use the Last.fm dataset, only this time we did not aggregate to the artist level. We kept the data in its disaggregated form, in which each row is an observation of a user listening to a song at a given time. We engineered features to add to this data, mostly using `timestamp`.

##### Feature Engineering
Within our Feature Engineering file you are able to see all the 24 features we created from out base data set. 

###### Timestamp Columns:

* daytime (morning, afternoon, evening, etc. There are 5 time blocks)
* weekday (monday= 0, tuesday = ,... sunday = 6)
* hour (integer hour of the day)
* weekend (weekday = 0, weekend = 1)
* quarter (fall, spring, summer, winter)
* month
* last seen song (last heard song by a user)
* last seen artist (last heard artist by a user)
	
###### Count Columns: 

* track-weekday-count (count of times a song was heard by the user over the weekday)
* user-artist-weeday-count (count of times an artist was heard by the user over the weekday)
* track-daytime-count (count of times a song was listened during a particular time of day)
* artist_total_count (cumulative count of times an artist was heard by all users)
* song_total_count (cumulative count of times a song was heard by all users)
* user-artist-count (cumulative count of times a song was heard by a particular user) 
* user-track-total-count (cumulative count of times an artist was heard by a particular user)

###### Skip Columns:

* user-song-skips (for each user cumulative skip per song counts, a skip is a song listened to for less than 1 minute)
* user-artist-skips (for each user cumulative skip per song counts)
* user-song-skip-percentage (`user-song-skips`/`user-track-total-count`) 
* user-artist-skip-percentage (`user-artist-skips`/`user-artist-count`)
* global-song-skips (cumulative count of songs skipped over all users)
* global-artist-skips (cumulative count of times an artist was skipped over all users)
* global-song-skip-percentage (`global-song-skips`/`song_total_count`)
* global-artist-skip-percentage (`global-artist-skips`/`song_total_count`)

###### Other Columns:

* age (age of user)
* gender (gender of user)

## Models

### Neural Network Implementation

#### Data Structure
We added a gender column assigning a 1 or 2 index based on the user's gender. Otherwise, we kept all other characteristics of the csv we created in the [Feature Engineering notebook](code/Feature Engineering.ipynb).

#### Imputation
Imputation was necessary for the neural network. There were many missing observations from songs new to a user. We imputed these values with zeroes. For most features, this imputation of zero is apropriate considering the feature's purpose. In the skip related column, a zero value means no skips. If we only had skip-related columns, then it might have been inapropriate to have new songs have a value of 0, as that would put them on par with songs that were listened to fully. However, songs listened to are treated differently than unheard songs in many other columns, and this allowed us to avoid the possible issues associated with our imputation. 

#### Model Exploration/Results
We trained the neural network using a validation set and tuned batch size, number of epochs, and the architecture. The chart below shows a few of our hyperparameters. We used AUC as evaluation metric for the validation set to help us choose our parameters. For our final neural network, we used a batch size of 256, epoch size 10, and used 25 input variables and 1 neuron in the hidden layer.

![neuralNetworkParam.jpeg](data/neuralNetworkParam.jpeg)

### SVD++ Implementation

#### Data Structure
Surprise requires the dataset to be in a tall format, with the matrix set up as _user, song, skipped_. To include periodicity, we needed to distinguish the period in which a song was listened while keeping the form required by Surprise. To do this, we concatenated `trackartist` with `period`.
![](data/period_preview.png)

Because we use periodicity, we needed to aggregate the data to the period level. For every user and song, we aggregate to weekday or weekend. This makes the `skipped` parameter a continuous value between 0 and 1, where 0 means the song was never skipped, 0.5 means the song was skipped half the times it was listened to, and 1 means the song was always skipped.

#### Imputation
We do not impute values in the SVD++ model as it automatically generates an implicit user-song matrix. This is a binary of whether or not a user has listened to the song in a given period.  This implicit matrix captures the missing values.

#### Model Exploration
We designed a user-song matrix and used `skipped` as our parameter of interest. The implicit factor _FY_ of SVD++ was then combined with the user-song latent space to form the reconstructed _(U+FY)V<sup>T</sup>_ matrix. This approach considers the act of skipping a song in a particular period to contain significant information about the user's preference and unspecified activity.

In the SVD model from Part I, we used a binary variable for whether the user had listened to an artist. Such a derivation of user factors does not discriminate between users who have listened to the same set of artists at different quantities. Two such users will have exactly the same song recommendation by the original SVD model.

We concatenated the period with the song name to incorporate a time factor in the SVD++ algorithm. This way the model predicts whether the user is likely to skip an individual song during a given period. The song name and period were combined with three underscores between them. Afterwards, when we were splitting the predictions dataset to calculate AUC, we dropped several song names because they contained three underscores within the name.

#### Model Results
We evaluated our model using the AUC: **0.81**, RMSE: **0.136**, and MAE: **0.03**. In addition, we used the *Surprise* package to compute RMSE and MAE on the same dataset for two benchmark algorithms. The NormalPredictor algorithm evaluated at RMSE: **0.137** and MAE: **0.07**, while the SGD algorithm attained RMSE: **0.1** and MAE: **0.03**.

While the AUC depends only on the rank order of the predicted probabilities, the RMSE fluctuates as the constant numbers are scaled.  For this reason, we focused primarily on using AUC to evaluate our model.

### Ensemble
We can combine the SVD++ model with the neural network in two ways:

Method 1: We combine the top K recommendations from the SVD++ model with the top K NN predictions, where the top songs are those with the lowest probability of being skipped.  The user is then shown these top K recommendation, half of which incorporate a novelty aspect and the other half incorporate the users' historical behavior.

Method 2: After running the SVD++ model and the neural network, we create two skip probability vectors for each user-song combination.  We then use a linear combination of these vectors to form our final output vector.  This vector can be thought of as an additional contextual feature about the users, which would be individually incorporated into a larger recommendation system that looks at other aspects music personalization.

SVD++ Weight | NN Weight | Ensemble AUC
--- | --- | ---
0.00 | 1.00 | 0.679
0.05 | 0.95 | 0.763
0.40 | 0.60 | 0.774
0.50 | 0.50 | 0.789
0.60 | 0.40 | 0.800
0.80 | 0.20 | 0.810
0.90 | 0.10 | 0.812
0.95 | 0.05 | 0.811
1.00 | 0.00 | 0.807

## Final Results
The neural network trains in a matter of minutes with a multitude of features, while the SVD++ model required several hours to train with only two features. Our SVD++ model significantly outpeformed the neural network model, which is why we weighted the SVD++ model as 90% of our combined linear ensemble. The neural network is 10% of the combined linear ensemble.

The AUC from the ensemble, **0.808**, is marginally higher than the SVD++ model alone AUC, **0.807**. The ensemble is significantly higher than the neural network AUC, **0.609**. An AUC of 0.8 suggests that we can leverage our ensemble model for music recommendations in a commercial setting. 

The neural network captured the probability of skipping only for songs previously heard by the user, while the SVD++ model made novel predictions. Since the ensemble consisted of 90% of the SVD++ model, we are able to include a larger numer of skip predictions for new songs.

## Lessons Learned
We restricted our SVD++ model to a single periodicity parameter (whether the song was listened to on a weekend or a weekday) as the size of the dataset grows rapidly with additional features. With more computing power, we could incorporate additional periodicity parameters (e.g. time of day, month, holidays) and tune the SVD++ hyperparameters.

We also experimented with using Spark. We wanted to use Spark because data engineering in Pandas is not always feasible with large datasets. However, we found the setup process to be entirely different for Windows and macOS users. As a result, we could not use consistent methods throughout our implementation. Moreover, Spark has a steep learning curve for feature engineering. We invested a significant amount of time to format our dataset and add new features – a process that is straightforward in Pandas. Additionally, Spark libraries have spotty documentation and do not have a full implementation of the SVD++ algorithm in Python. We attempted to craft the algorithm from scratch using matrix factorization and stochastic gradient descent operations, but found it prohibitive to experiment with hyperparameters given the size of the dataset. We managed to implement the neural network on Spark (ml library's multi-layer perceptron implementation), but the setup was not configured appropriately for our local machines, therefore the model would not train. We finally resorted to using Tensorflow for the NN.
