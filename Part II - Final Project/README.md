# Final Project

## Introduction
We designed a recommender system that predicts a user's probability of skipping a song. We created a `skipped` parameter that identifies whether a user skipped the song. Specifically, if a user listens to a song for less than sixty seconds, we consider that to be a skip.

In our review of various recommendation engines that are based on users’ listening habits, we have not encountered an approach that modeled the users’ skip preferences. We believe this parameter adds significant value as it helps us understand the users’ preference for a song based on implicit data. It may be that the user has grown tired of the song and no longer wants to hear it, but it can also be the case that the user is in a different listening mood and prefers to listen to something else. This has been the primary motivation for incorporating skips.

### Approach
We chose to build a hybrid model using a neural network and SVD++.

The neural network incorporates user's past preferences and recency into the model, identifying how user preferences shift over the duration of their listening history. Additionally, the neural network identifies the factors that affect the users' decision to skip a song.

Our SVD++ model incorporates periodicity. It also incorporates songs that the user has not yet heard, or songs in a new period, by identifying similarities in the latent space. We modified our ratings matrix to include skips and to incorporate a period for each song: whether or not it was the weekend. The SVD++ approach is a more complex version of the SVD baseline model from Part I. The model adds an implicit user-factor matrix to adjust the explicit user-factor matrix.

Since both models output a vector of the probability a user will skip a song, we chose to run the models independently and combine the probabilities afterwards, hoping that the combined probability would improve the model's accuracy.

### Data
We continued to use the Last.fm dataset, only this time we did not aggregate to the artist level. We kept the data in its disaggregated form, in which each row is an observation of a user listening to a song at a given time. 

The dataset contained over 170K unique tracks and 1K users. However a large number of these songs are never listened to more than a handful of times across all the users in the entire dataset. To prune this down, we considered the top 500 songs listened by each user for our analysis. 

We engineered features to add to this data, mostly using `timestamp`.


### Model Evaluation Strategy
We split our dataset into train, validation and testing datasets. **The split was done based on timestamps**. The training data contained the first 70% of each user's listening history. The validation set has the next 15% and the testing set has the final 15% of the history. 

The models were trained on the training data, tuned using the evaluation data and the performance is finally reported based on predicitons on the test data.


### Feature Engineering
Our base data set contained the complete listening history of 1K users. Using that we engineered the features described below. All feature engineering was done in a cumulative manner **incorporating only past data at each point**. This was done to ensure that there is **no leakage of data from the future** for prediction purposes.

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

###### Other Columns - from metadata:

* age (age of user)
* gender (gender of user)

## Models

### Neural Network Implementation

#### Data Structure
We added a gender column assigning a 1 or 2 index based on the user's gender. Otherwise, we kept all other characteristics of the csv we created in the [Feature Engineering notebook](code/Feature Engineering.ipynb).

#### Imputation
Imputation was necessary for the neural network as it can't handle missing values. Missing values primarily arise in the validation/test set for new artists of songs that the user listens to. We imputed these values with zeroes. For most features, this imputation of zero is appropriate considering the feature's purpose. In the skip related column, a zero value means no skips. 

#### Model Tuning
We trained the neural network using a validation set and tuned batch size, number of epochs, and the architecture. The chart below shows a few of our hyperparameters. We used AUC as evaluation metric for the validation set to help us choose our parameters. 

![neuralNetworkParam.jpeg](data/neuralNetworkParam.jpeg)

We observed that the model was very sensitive to overfitting and increasing the complexitiy resulted in deterioration of the validation AUC. So decided to keep the model simple. 

We also experimented with the choice of optimizer. Moving from SGD to AdaGrad gave a significant lift to the AUC. Our final model has one hidden layer with 2 neurons with ReLU activation trained with AdaGrad optimizer for 5 epochs of batch size 256.  

#### Model Results

The final model has a validation AUC of **0.705** and test AUC of **0.68**. 

This is lower than the benchmark AUC of 0.759. The primary reason for this the way we engineered our features. We used a cumulative strategy for all variables to avoid drawing any inferences from future timestamps resulting in data leakage. This feature engineering strategy implies that the training data contains many data points for which the user's complete behavior is not fully noted (for example the first few days of usage). Since these points are also used in the training of the model, the predictions are of a lower quality.

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
We created an ensemble of the two models - SVD++ and the Neural Network to obtain better recommendations. The rationale behind this choice is that SVD++ captures similarities among users and can provide novel recommendations wheras the Neural Network is trained on the users' historic behavior to predict their likelihood of a skipping a song based on past behavior.

Our method of ensembling the model is to use a simple linear combination of the predicitons from both the models.

![Ensemble contribution](data/ensemble.png)

We looked at different weghted averages of the model to assess the relative performace. Based on the observations, we decided to use an ensemble with 90% SVD++ contribution and 10% NN contribution for the final model.



## Model Utility

Music recommendation involves numerous problems and we tried to address one of them in this project - likelihood of users skipping songs. The ensemble model predicts this probability for the users for a given song. The two models in the ensemble address this in distinct ways - The Neural Network is trained on the historical behavior of the users and the SVD++ looks at a broader scope of identifying similarities between users. 

The model can be utilized in two ways in a commercial music personalization setting:

**Method 1 - Standalone** : We recommend the top K recommendations from the model to a user, where the top songs are those with the lowest probability of being skipped. The model incorporates both the user's historic preferences and behavior as well as novel predictions based on the preference of similar users. 

**Method 2 - Broader Personalization System** : The ensemble enables us to create a probability vector for each user-song combination. This vector can be thought of as an additional contextual feature about the users, which would be incorporated into a larger recommendation system that looks at other aspects music personalization.



## Final Results
The neural network trains in a matter of minutes with a multitude of features, while the SVD++ model required several hours to train with only two features. Our SVD++ model significantly outpeformed the neural network model, which is why we weighted the SVD++ model as 90% of our combined linear ensemble. The neural network is 10% of the combined linear ensemble.

The AUC from the ensemble, **0.808**, is marginally higher than the SVD++ model alone AUC, **0.807**. The ensemble is significantly higher than the neural network AUC, **0.609**. An AUC of 0.8 suggests that we can leverage our ensemble model for music recommendations in a commercial setting. 

The neural network captured the probability of skipping only for songs previously heard by the user, while the SVD++ model made novel predictions. Since the ensemble consisted of 90% of the SVD++ model, we are able to include a larger numer of skip predictions for new songs.

## Lessons Learned
We restricted our SVD++ model to a single periodicity parameter (whether the song was listened to on a weekend or a weekday) as the size of the dataset grows rapidly with additional features. With more computing power, we could incorporate additional periodicity parameters (e.g. time of day, month, holidays) and tune the SVD++ hyperparameters.

We also experimented with using Spark. We wanted to use Spark because data engineering in Pandas is not always feasible with large datasets. However, we found the setup process to be entirely different for Windows and macOS users. As a result, we could not use consistent methods throughout our implementation. Moreover, Spark has a steep learning curve for feature engineering. We invested a significant amount of time to format our dataset and add new features – a process that is straightforward in Pandas. Additionally, Spark libraries have spotty documentation and do not have a full implementation of the SVD++ algorithm in Python. We attempted to craft the algorithm from scratch using matrix factorization and stochastic gradient descent operations, but found it prohibitive to experiment with hyperparameters given the size of the dataset. We managed to implement the neural network on Spark (ml library's multi-layer perceptron implementation), but the setup was not configured appropriately for our local machines, therefore the model would not train. We finally resorted to using Tensorflow for the NN.
