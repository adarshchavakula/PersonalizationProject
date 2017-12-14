# Final Project
_**NOTE:** high level summary will go into the readme, this is the detailed writeup of our project. Think of this as our academic paper and the high level summary as a one pager._
## Introduction
We are designing a recommendation system that incorporates the users’ likelihood to skip a song into the final output.  We have designed a skips parameter based on whether the user has listened to the song for more than 60 seconds.  In other words, if the user stopped listening to the song before the 60 second timepoint, we consider the song to be skipped.

In our literature review of various recommendation engines that are based on the users’ listening habits, we have not encountered an approach that modeled the users’ skip preferences.  We believe this parameter to add significant value as it helps us understand the users’ preference for a song based on an unspecified activity.  It may be that the user has grown tired of the song and no longer wants to hear it, but it can also be the case that the user is in a different listening mood and prefers to listen to something else.  This has been the primary motivation for incorporating skips.

### Approach
***What did we want to do? What was our plan?***

We chose to build a hybrid model using a neural network and SVD++. The neural network would incorporate recency into the model, identifying how user preferences shift over the duration of the dataset and identifying latent features that affect a user's decision to skip a song. Meanwhile, SVD++ would incorporate periodicity, identifying when a user enjoys a song in a given period. We also believed SVD++ would better capture songs that a user has not yet listened to, or songs in a new period, by identifying similarities in the latent space.

Because both models output a vector of the probability a user will skip a song, we chose to run the models independently and combine the probabilities afterwards, hoping that the combined probability would improve the model's predictive power.

### Data
***Introduce the data, maybe provide some summary stats?***

We continued to use the Last.fm dataset, only this time we did not aggregate to the artist level. We instead kept the data in its disaggregated form, where each row is an observation of a user listening to a song at a given time. We engineered features to add to this data, mostly using the timestamp.

##### Feature Engineering
***Show new features and how we engineered them, particularly the predicted variable.***

### Models

##### Neural Network
***High level plan***

##### SVD++
***High level plan***

##### Performance Evaluation

## Models

### Neural Network Implementation

#### Data Structure
***From the base dataset, did you do any other data prep?***

#### Imputation
***What did you impute? Why? If not, why not? Does that affect the model?***

#### Model Exploration
***So you ran the model. How? What choices did you have to make and why did you make them?***

#### Model Results
***Final results?***

### SVD++ Implementation

#### Data Structure
Surprise requires the dataset to be in a tall format, with the matrix set up as _user-song-skipped_. To include periodicity, we need to distinguish the period in which a song was listened while keeping the form required by Surprise. To do this, we concatenated `trackartist` with `period`.

***Provide a preview of the dataframe***

#### Imputation
Imputation is not necessary for this model. SVD++ creates an implicit matrix, a binary of whether or not a user has listened to a song in a period. This implicit matrix captures the missing values.

#### Model Exploration
***So you ran the model. How? What choices did you have to make and why did you make them?***

#### Model Results
***Final results?***

### Ensemble
***How did we combine the results? How did the hybrid do?***

## Final Results
***Performance (both time and accuracy)***

***Would we use this? Does this model perform better on some users/songs than others?***

## Lessons
***What did we learn? What might we do if you continue to work on this or had more time? We can talk about the models individually here but we should write something cohesive as well.***
