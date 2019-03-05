def tidyup_video_features(openface_features, PID, EXP):
    # tidy up data frame:
    filter_col = [col for col in openface_features if col.startswith('AU')]
    filter_col.insert(0,'time')
    filter_col.insert(0,'participant_id')
    filter_col.insert(0,'experiment_id')
    openface_features['participant_id'] = PID
    openface_features['experiment_id'] = EXP
    openface_features = openface_features[filter_col]
    openface_features.columns = openface_features.columns.str.replace('_', '')
    openface_features = openface_features.rename(columns = {'experimentid':'experiment_id'})
    openface_features = openface_features.rename(columns = {'participantid':'participant_id'})
    return openface_features
