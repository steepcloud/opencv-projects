#include "mainwindow.h"
#include <filesystem>
#include <iostream>

// TODO:
// - implement word-wrap function

Mat loadImage(const std::string &fileName) {
    Mat image = imread(fileName, IMREAD_UNCHANGED);

    if (image.empty()) {
        qDebug() << "Couldn't load " << QString::fromStdString(fileName);
    }

    return image;
}

void overlayImage(const cv::Mat &background, const cv::Mat &foreground,
                  cv::Mat &output, cv::Point2i location)
{
    background.copyTo(output);

    // start at the row indicated by location, or at row 0 if location.y is negative.
    for(int y = std::max(location.y , 0); y < background.rows; ++y)
    {
        int fY = y - location.y; // because of the translation

        // we are done if we have processed all rows of the foreground image.
        if(fY >= foreground.rows)
            break;

        // start at the column indicated by location,
        // or at column 0 if location.x is negative.
        for(int x = std::max(location.x, 0); x < background.cols; ++x)
        {
            int fX = x - location.x; // because of the translation.

            // we are done with this row if the column is outside of the foreground image.
            if(fX >= foreground.cols)
                break;

            // determine the opacity of the foreground pixel, using its fourth (alpha) channel.
            double opacity =
                ((double)foreground.data[fY * foreground.step + fX * foreground.channels() + 3]) / 255.;

            // combine the background and foreground pixel, using the opacity,
            // but only if opacity > 0.
            for(int c = 0; opacity > 0 && c < output.channels(); ++c)
            {
                unsigned char foregroundPx =
                    foreground.data[fY * foreground.step + fX * foreground.channels() + c];
                unsigned char backgroundPx =
                    background.data[y * background.step + x * background.channels() + c];
                output.data[y*output.step + output.channels()*x + c] =
                    backgroundPx * (1.-opacity) + foregroundPx * opacity;
            }
        }
    }
}

void MainWindow::addSpeechBubble(Mat &parentImage, Mat &spcBubble, const string &text, Rect roi, bool flipB, VideoWriter &video) {
    Mat myBubble = spcBubble;

    // vertical flip
    if (flipB) {
        flip(spcBubble, myBubble, 1);
    }

    // resize the bubble to fit ROI
    Mat resizedBubble;
    cv::resize(myBubble, resizedBubble, Size(roi.width, roi.height), INTER_LINEAR);

    // defining the region of interest for the speech bubble
    Mat originalROI = parentImage(roi).clone(); // storing the original ROI for later

    // gradual appearance of speech bubble
    double alpha = 0.0;
    while (alpha <= 1.0) {
        Mat overlay;

        // using the overlayImage function instead of addWeighted
        overlayImage(originalROI, resizedBubble, overlay, Point(0, 0));
        overlay.copyTo(parentImage(roi));

        video.write(parentImage);

        imshow("Conversation", parentImage);

        waitKey(100);
        alpha += 0.1;
    }

    // rendering text letter by letter
    int textLength = text.length();
    string procText = "";

    for (int i = 0; i < textLength; i++) {
        procText += text[i];

        putText(parentImage, procText, Point(roi.x + 50, roi.y + 70), FONT_HERSHEY_SIMPLEX, 0.6, Scalar(255, 255, 255), 1);

        video.write(parentImage);

        imshow("Conversation", parentImage);
        waitKey(150);
    }

    // keep it visible for a sec
    waitKey(1000);

    // gradual disappearance of speech bubble
    alpha = 1.0;
    while (alpha >= 0.0) {
        Mat overlay;

        // using the overlayImage function for gradual disappearance
        overlayImage(resizedBubble, originalROI, overlay, Point(0, 0));
        overlay.copyTo(parentImage(roi));

        // clear text
        putText(parentImage, "", Point(roi.x + 50, roi.y + 70), FONT_HERSHEY_SIMPLEX, 1, Scalar(255, 255, 255), 2);

        video.write(parentImage);

        imshow("Conversation", parentImage);

        waitKey(100);
        alpha -= 0.1;
    }
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // for debug purposes
    cout << "Current working directory: " << filesystem::current_path() << endl;

    Mat conversation = loadImage("conversation.png");
    Mat textBubble = loadImage("textbbl.png");

    if (conversation.empty() || textBubble.empty()) {
        return;
    }

    // defining ROI for speech bubbles (x, y, width, height)
    Rect batmanBubbleRect(200, 40, 300, 150);
    Rect robinBubbleRect(700, 20, 300, 150);

    VideoWriter video("conversation.mp4", VideoWriter::fourcc('X', 'V', 'I', 'D'), 10, conversation.size());

    // actors' speech
    addSpeechBubble(conversation, textBubble, "We must act!", batmanBubbleRect, false, video);
    addSpeechBubble(conversation, textBubble, "What's the plan, Bats?", robinBubbleRect, true, video);
    addSpeechBubble(conversation, textBubble, "No plan. Just justice.", batmanBubbleRect, true, video);
    addSpeechBubble(conversation, textBubble, "Hell yeah. Let's roll.", robinBubbleRect, true, video);

    video.release();

    destroyWindow("Conversation");
}

MainWindow::~MainWindow() {}
