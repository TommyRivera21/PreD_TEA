import React, { useState, useRef, useEffect } from "react";
import { useParams } from "react-router-dom";
import styles from "../styles/VideoScanning.module.css";
import videoSrc from "../assets/video-diagnostico-autismo.mp4";
import { uploadVideo } from "../services/api";
import { getCurrentToken } from "../services/authService";

const VideoScanning: React.FC = () => {
  const { diagnosticId } = useParams<{ diagnosticId: string }>();
  const [countdown, setCountdown] = useState(5);
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const videoRef = useRef<HTMLVideoElement>(null);
  const webcamRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    } else if (countdown === 0) {
      startWebcamAndRecording();
    }
  }, [countdown]);

  const startWebcamAndRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (webcamRef.current) {
        webcamRef.current.srcObject = stream;
      }
      startRecording(stream);
    } catch (err) {
      console.error("Error accessing webcam:", err);
    }
  };

  const startRecording = async (stream: MediaStream) => {
    try {
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: "video/webm",
      });

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        if (chunksRef.current.length > 0) {
          const blob = new Blob(chunksRef.current, { type: "video/webm" });
          chunksRef.current = [];

          const formData = new FormData();
          formData.append("video", blob, "recording.webm");

          if (diagnosticId) {
            formData.append("diagnostic_id", diagnosticId);
          } else {
            console.error("No diagnostic ID available");
            return;
          }

          try {
            const token = getCurrentToken();
            if (!token) {
              throw new Error("No authentication token found");
            }

            const response = await uploadVideo(
              formData,
              parseInt(diagnosticId)
            );
            console.log("Video uploaded successfully:", response);

            window.location.href = `/questionnaire/${diagnosticId}`;

          } catch (error) {
            console.error("Error uploading video:", error);
          }
        } else {
          console.error("Not enough segments to upload");
        }
      };

      mediaRecorderRef.current.start(1000);
      setIsRecording(true);
      timerRef.current = window.setInterval(
        () => setRecordingTime((prev) => prev + 1),
        1000
      );
    } catch (error) {
      console.error("Error starting recording:", (error as Error).message);
    }
  };

  const handlePauseRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.pause();
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      setIsPaused(true);
    }
  };

  const handleResumeRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "paused"
    ) {
      mediaRecorderRef.current.resume();
      timerRef.current = window.setInterval(
        () => setRecordingTime((prev) => prev + 1),
        1000
      );
      setIsPaused(false);
    }
  };

  const handleStopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      setIsRecording(false);
      setIsPaused(false);
      setRecordingTime(0);
    }
  };

  useEffect(() => {
    return () => {
      if (
        mediaRecorderRef.current &&
        mediaRecorderRef.current.state !== "inactive"
      ) {
        mediaRecorderRef.current.stop();
      }
      if (webcamRef.current && webcamRef.current.srcObject) {
        const tracks = (webcamRef.current.srcObject as MediaStream).getTracks();
        tracks.forEach((track) => track.stop());
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${minutes.toString().padStart(2, "0")}:${seconds
      .toString()
      .padStart(2, "0")}`;
  };

  return (
    <div className={styles.videoScanning}>
      <h1 className={styles.titleDiagnostic}>Diagnóstico por video</h1>
      {countdown > 0 ? (
        <div>
          <p className={styles.countdown}>Iniciando en: {countdown}</p>
        </div>
      ) : (
        <div className={styles.videoContainer}>
          <video
            ref={videoRef}
            src={videoSrc}
            autoPlay
            controls
            className={styles.mainVideo}
          />
          <div className={styles.webcamContainer}>
            {isRecording && (
              <div className={styles.overlay}>
                <span className={styles.recordingIndicator}>●</span>
                <p className={styles.recordingTime}>
                  {formatTime(recordingTime)}
                </p>
              </div>
            )}
            <video ref={webcamRef} autoPlay className={styles.webcamFeed} />
            <div className={styles.buttonContainer}>
              {isRecording && !isPaused && (
                <button
                  onClick={handlePauseRecording}
                  className={styles.pauseButton}
                >
                  Pausar grabación
                </button>
              )}
              {isRecording && isPaused && (
                <button
                  onClick={handleResumeRecording}
                  className={styles.resumeButton}
                >
                  Reanudar grabación
                </button>
              )}
              {isRecording && (
                <button
                  onClick={handleStopRecording}
                  className={styles.stopButton}
                >
                  Finalizar grabación
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoScanning;
