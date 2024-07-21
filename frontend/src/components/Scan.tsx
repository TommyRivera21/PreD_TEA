import React, { useState } from "react";
import styles from "../styles/Scan.module.css";
import { createDiagnostic } from "../services/api";

const Scan: React.FC = () => {
  const [error, setError] = useState<string | null>(null);

  const handleCreateDiagnostic = async (scanType: "video" | "image") => {
    try {
      const diagnosticResponse = await createDiagnostic(scanType);

      if (diagnosticResponse.diagnostic_type === "video") {
        window.location.href = `/video-scanning/${diagnosticResponse.id}`;
      } else if (diagnosticResponse.diagnostic_type === "image") {
        window.location.href = `/image-scanning/${diagnosticResponse.id}`;
      } else {
        throw new Error("Tipo de diagnóstico no válido");
      }
    } catch (error) {
      console.error("Error creating diagnostic:", error);
      setError("Error al crear el diagnóstico. Por favor, intente de nuevo.");
    }
  };

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.scan}>
      <h1 className={styles.titleDiagnosticType}>
        Seleccione el tipo de diagnóstico
      </h1>
      <div className={styles.scanOptions}>
        <button
          onClick={() => handleCreateDiagnostic("video")}
          className={styles.btnScan}
        >
          Diagnostico por Video
        </button>
        <button
          onClick={() => handleCreateDiagnostic("image")}
          className={styles.btnScan}
        >
          Diagnostico por Imágenes
        </button>
      </div>
    </div>
  );
};

export default Scan;
