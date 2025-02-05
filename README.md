# NeuroGrip: EEG-Based Controlled Robotic Arm

## Overview

**NeuroGrip** is an advanced EEG-based brain-machine interface (BMI) system designed to control a robotic arm using intuitive motor imagery. Inspired by the paper *Brain-Controlled Robotic Arm System Based on Multi-Directional CNN-BiLSTM Network Using EEG Signals*, this project leverages deep learning techniques to decode EEG signals and translate them into real-time robotic arm movements.

## Features

- **Brain-Machine Interface (BMI):** Uses EEG signals for intuitive robotic arm control.
- **Multi-Directional Control:** Allows movement in six directions (left, right, forward, backward, up, down).
- **Deep Learning Model:** Implements a Multi-Directional CNN-BiLSTM (MDCBN) network for high-accuracy EEG signal decoding.
- **Real-Time Control:** Provides a continuous decoding strategy for seamless robotic arm operation.
- **Motor Imagery-Based Execution:** Users can control the arm through imagined movements.

## System Architecture

The NeuroGrip system consists of the following components:

1. **EEG Data Acquisition:** Captures brain signals using an EEG headset.
2. **Preprocessing:** Filters and cleans the EEG signals for noise reduction.
3. **Deep Learning Model:**
   - CNN extracts spatial EEG features.
   - BiLSTM captures temporal dependencies for movement prediction.
4. **Robotic Arm Control:** Maps decoded signals to robotic arm movements.
5. **Feedback Mechanism:** Provides real-time updates for movement accuracy.

## Usage

1. Wear the EEG headset and ensure proper electrode placement.
2. Calibrate the system by recording baseline EEG signals.
3. Perform motor imagery of arm movements (left, right, forward, backward, up, down).
4. Observe the robotic arm replicating the imagined movements.

## Dataset

- EEG signals are recorded from multiple subjects.
- Data is preprocessed and labeled based on movement intention.
- Model is trained using supervised learning techniques.

## Performance Metrics

- **Correlation Coefficient (CC):** Measures accuracy between predicted and actual movement.
- **Normalized Root Mean Square Error (NRMSE):** Evaluates prediction error.
- **Success Rate:** Determines real-time control efficiency.

## Future Improvements

- Optimize deep learning model for better accuracy.
- Enhance real-time processing speed.
- Expand to control additional robotic functionalities.
- Improve user training for better EEG signal quality.

## References

- *Brain-Controlled Robotic Arm System Based on Multi-Directional CNN-BiLSTM Network Using EEG Signals*, IEEE Transactions on Neural Systems and Rehabilitation Engineering, 2020.

## Contributors

- **Anto Rishath** - CB.SC.U4AIE23103
- **Arunoday A K** - CB.SC.U4AIE23106
- **Achutharaj R** - CB.SC.U4AIE23108
- **Vijay Santhosh P** - CB.SC.U4AIE23157
- **Yashwanth P T** - CB.SC.U4AIE23164

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Special thanks to researchers and contributors in the field of BMI and EEG-controlled robotics.
