#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <string>

void opticalFlow(cv::Mat &prevGray, cv::Mat &currGray, cv::Mat &flow, cv::Mat &mask) {

    //farneback optical flow: basic and efficient

    // params:
    // previous, next, pyramindflow, levels, winsize, iterations, poly_n, poly_sigma, flags, flow
    cv::calcOpticalFlowFarneback(prevGray, currGray, flow, 0.5, 3, 15, 3, 5, 1.2, 0);


    cv::Mat flowParts[2]; // x y split
    split(flow, flowParts);
    cv::Mat magnitude, angle;

    cv::cartToPolar(flowParts[0],flowParts[1], magnitude, angle, true); // do it in degrees

    double maxVal;
    cv::minMaxLoc(magnitude, 0, &maxVal);
    double thresh = 0.5 * maxVal; // This threshold can be tuned.
    cv::threshold(magnitude, mask, thresh, 255, cv::THRESH_BINARY_INV);
    mask.convertTo(mask, CV_8U);
}


cv::Mat affineTransFromFlow(cv::Mat &flow, cv::Mat &mask) {

    
    std::vector<cv::Point2f> srcPoints, dstPoints;

    // samople
    for (int y= 0; y<mask.rows; y++)
    {
        for (int x= 0; x < mask.cols; x++){
            if(mask.at<uchar>(y, x) > 0) {
                cv::Point2f pt(x, y);
                // Get the displacement from the flow field.
                cv::Point2f d = flow.at<cv::Point2f>(y, x);
                srcPoints.push_back(pt);
                dstPoints.push_back(pt + d);
            }
        }
    }

    cv::Mat affine;

    if (srcPoints.size()<100){
        affine = cv::estimateAffinePartial2D(srcPoints, dstPoints, cv::noArray(), cv::RANSAC);
    } else {
        affine = cv::Mat::eye(2,3, CV_64F);
    }

    return affine;
}

cv::Mat stabilize(cv::Mat &affine, cv::Mat &frame) {
    cv::Mat stabilizedFrame;
    warpAffine(frame, stabilizedFrame, affine, frame.size(), cv::INTER_LINEAR, cv::BORDER_CONSTANT, cv::Scalar(0, 0, 0));
    return stabilizedFrame;
}

cv::Mat inPaint(cv::Mat &frame) {
    cv::Mat gray, mask;
    cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
    cv::threshold(gray, mask, 10, 255, cv::THRESH_BINARY_INV);
    cv::Mat inpainted;
    cv::inpaint(frame, mask, inpainted, 3, cv::INPAINT_TELEA);
    return inpainted;
}

cv::Mat iterativeProcessing(cv::Mat &frame, cv::Mat &prevGray){
    cv::Mat blank;
    return blank;
}

int main (int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Error: Not enough arguments provided." << '\n';
        std::cerr << "Usage: ./videostabilizer <inputPath> <outputPath>" << '\n';
        return -1;
    }



    std::string inputPath = argv[1];
    std::string outputPath = argv[2];
    // error check
    cv::VideoCapture cap(inputPath);
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open video file." << '\n';
        return -1;
    }

    // get basic frame info
    int w = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    int h = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    double fps = cap.get(cv::CAP_PROP_FPS);

    //writer out
    cv::VideoWriter writer(outputPath, cv::VideoWriter::fourcc('m', 'p', '4', 'v'), fps, cv::Size(w, h));
    // error check
    if(!writer.isOpened()) {
        std::cerr<<"Error: Writer could not open and write file" << '\n';
        return -1;
    }
    cv::Mat prevframe, prevGray;
    cap >> prevframe;

    // error check
    if(prevframe.empty()){
        std::cerr << "Error: Previous frame is empty, possibly file corrupted." << '\n';
        return -1;
    }

    cv::cvtColor(prevframe, prevGray, cv::COLOR_BGR2GRAY); //convert to grayscale


    while(true){
        cv::Mat currFrame, currGray;
        cap >> currFrame;
        if(currFrame.empty()){
            std::cerr << "Frame empty, processing ended. " << '\n';
            break;
        }
        // convert and make gray frame
        cv::cvtColor(currFrame, currGray, cv::COLOR_BGR2GRAY);

        cv::Mat flow, mask;

            opticalFlow(prevGray, currGray, flow, mask);

            // affine transformations (preserve lines and edges to reduce major warping)
            cv::Mat affineMat = affineTransFromFlow(flow, mask);

            // Stabilize frame algo

            cv::Mat stabilizedFrame = stabilize(affineMat, currFrame);


        // outpaint borders: fill frame:
        cv::Mat finalFrame = inPaint(stabilizedFrame);

        //prev

        cv::Mat finalGray;
        cv::cvtColor(finalFrame, finalGray, cv::COLOR_BGR2GRAY);
        prevGray = finalGray.clone();
        // output 
        writer.write(finalFrame);
    }
    cap.release();
    writer.release();
    cv::destroyAllWindows();
    std::cout << "Stabilization complete. Output saved as finished.mov" << '\n';
    return 0;


}