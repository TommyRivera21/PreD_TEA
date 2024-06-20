import React, { useState, useRef, useEffect } from 'react';

const Scan: React.FC = () => {
  const [countdown, setCountdown] = useState(10);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const getVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error(err);
      }
    };

    getVideo();
  }, []);

  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  return (
    <div>
      <h1>Escaneo de Expresiones</h1>
      {countdown > 0 ? (
        <div>
          <p>Iniciando en: {countdown}</p>
        </div>
      ) : (
        <div>
          <video ref={videoRef} autoPlay></video>
          {/* Aquí agregar la lógica para grabar el video */}
        </div>
      )}
    </div>
  );
};

export default Scan;
