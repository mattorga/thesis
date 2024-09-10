def simulate(root_path):
   from opensim import opensim
   import os

   '''
   OpenSim Basic Visualizer

   Pre-requisites:
   - Geometry Folder: contains the joints that can be rendered
   - Pose2Sim Model: contains configurations for visualization
      - Ex. Pose2Sim_LSTM.osim, Pose2Sim_BODY25.osim
   - Pose2Sim Output Tracefile: contains coordinates of the joints over time
      - Pose2Sim outputs [.trc] -> OpenSim needs [.sto], just rename extension

   Usage:
   - Activate environment containing OpenSim
   - Run the script

   Issue:
   1. Pose2Sim Model: it should correspond to the person's physical properties [05/04/2024]
      - For now, a generic model is being used (i.e. Pose2Sim Default Models) 
   2. File paths are hard coded, need to optimize [05/06/2024]
   '''

   # Load the Model
   model = "Pose2Sim_LSTM.osim" # Avoid hard coding filenames
   model_path = os.path.join(root_path, model) 
   Model = opensim.Model(model_path)

   # Test input files: "walking.sto", "boxing.sto"
   sim_file = "walking.sto" # Avoid hard coding filenames
   sim_path = os.path.join(root_path, sim_file)
   time = opensim.TimeSeriesTable(sim_path)

   opensim.VisualizerUtilities.showMotion(Model,time)
      