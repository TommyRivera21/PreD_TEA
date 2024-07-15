import React, { useState } from "react";
import { useParams } from "react-router-dom";
import styles from "../styles/ImageScanning.module.css";
import { uploadImages } from "../services/api";

const ImageScanning: React.FC = () => {
  const { diagnosticId } = useParams<{ diagnosticId: string }>();
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedFiles(event.target.files);
  };

  const handleUpload = async () => {
    if (!diagnosticId) {
      console.error('No diagnostic ID available');
      return;
    }

    if (selectedFiles) {
      const formData = new FormData();
      Array.from(selectedFiles).forEach((file) => {
        formData.append('image', file);
      });
      formData.append('diagnosticId', diagnosticId); 

      try {
        const response = await uploadImages(formData, parseInt(diagnosticId));
        console.log('Images uploaded successfully:', response);
      } catch (error) {
        console.error('Error uploading images:', error);
      }
    }
  };

  return (
    <div className={styles.imageScanning}>
      <h1 className={styles.titleDiagnostic}>Diagnóstico por imágenes</h1>
      <div className={styles.instructions}>
        <input
          type="file"
          className={styles.uploadImages}
          multiple
          onChange={handleFileChange}
        />
        <button className={styles.confirmButton} onClick={handleUpload}>
          Subir imágenes
        </button>
      </div>
      {selectedFiles && (
        <div className={styles.imageGrid}>
          {Array.from(selectedFiles).map((file, index) => (
            <img
              key={index}
              src={URL.createObjectURL(file)}
              alt={`Preview ${index + 1}`}
              className={styles.previewImage}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ImageScanning;
