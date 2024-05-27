def calibrate(session_path):
    import os
    from Pose2Sim import Pose2Sim # type: ignore
    import toml
    import sys
    
    """
    CALIBRATION
        - Ideally, can only be done once to avoid variability between trials
    """

    config_path = os.path.join(session_path,"Config.toml")
    config_dict = toml.load(config_path)
    config_dict.get("project").update({"project_dir":"."})
    
    Pose2Sim.calibration(config_dict, session_path)
    
    """
    TO-DO

    # SINGLE PERSON
    
    participant = "S01_P01_Dom"
    participant_dir = os.path.join(session_dir, participant_dir) 

    trial = "S01_P01_T01"
    trial_dir = os.path.join(participant_dir, trial)

    project_dir = os.path.join(participant_dir, trial) #S00_P00_SingleParticipant\S00_P00_T00_StaticTrial
    config_dict.get("project").update({"project_dir":project_dir})
    config_dict['filtering']['display_figures'] = False

    Pose2Sim.personAssociation(config_dict)
    Pose2Sim.triangulation(config_dict)
    Pose2Sim.filtering(config_dict)
    Pose2Sim.markerAugmentation(config_dict)
    
    """