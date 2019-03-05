def tidyup_audio_features(librosa_features, PID, EXP):
    librosa_features['participant_id'] = PID
    librosa_features['experiment_id'] = EXP
    librosa_features = librosa_features.rename(columns={'zrc': 'zcrate'})
    librosa_features.drop(['timestamp'], axis = 1, inplace = True, errors = 'ignore')
    librosa_features = librosa_features[['participant_id','experiment_id','time','pitch','rmse','zcrate']]
    return librosa_features
