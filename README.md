### Motion Detection

This is a Python program that detects motion in a video stream using OpenCV. The program uses the background subtraction algorithm to detect motion and draws bounding boxes around the moving objects.

### Video Stabilization

The video stabilization implementation is based on the ICCV 2023 paper "Fast Full-frame Video Stabilization with Iterative Optimization" by Zhao et al. This approach provides real-time stabilization while maintaining high-quality frame preservation.

#### How It Works

1. **Motion Extraction**

   - The algorithm analyzes consecutive frames to compute motion trajectories
   - Features are detected using FAST (Features from Accelerated Segment Test) corners
   - KLT (Kanade-Lucas-Tomasi) tracking is employed to track these features across frames

2. **Stabilization Process**

   - **Motion Estimation**:
     - Extracts camera motion by analyzing feature correspondences
     - Computes homography matrices between consecutive frames
   - **Path Optimization**:
     - Implements iterative optimization to smooth camera paths
     - Uses a sliding window approach for real-time processing
     - Minimizes both trajectory smoothness and content preservation

3. **Frame Transformation**
   - Applies computed transformations to stabilize frames
   - Maintains frame boundaries to minimize empty borders
   - Uses edge-aware interpolation for high-quality frame warping

#### Key Features

- Real-time processing capability
- Minimal computing resource requirements
- Adaptive smoothing based on motion intensity
- Preservation of intentional camera movements
- Reduction of high-frequency jitter

The implementation provides a balance between stabilization quality and processing speed, making it suitable for real-time applications while maintaining professional-grade output quality.
