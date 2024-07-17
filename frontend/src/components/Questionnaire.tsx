import React, { useState, useEffect } from "react";
import styles from "../styles/Questionnaire.module.css";
import { questions, answers } from "../utils/itemsQuestionnaire";
import { useParams } from "react-router-dom";
import { submitQuestionnaire } from "../services/api";

const Questionnaire: React.FC = () => {
  const { diagnosticId } = useParams<{ diagnosticId?: string }>();
  const [responses, setResponses] = useState<string[]>(
    Array(questions.length).fill("")
  );
  const [error, setError] = useState<string>("");

  useEffect(() => {
    console.log("Diagnostic ID:", diagnosticId);
  }, [diagnosticId]);

  const handleResponseChange = (index: number, value: string) => {
    const newResponses = [...responses];
    newResponses[index] = value;
    setResponses(newResponses);
  };

  const handleSubmit = async () => {
    if (!diagnosticId) {
      console.error("Diagnostic ID is undefined.");
      return;
    }

    // Convertir a número
    const parsedDiagnosticId = parseInt(diagnosticId, 10);

    if (responses.some((response) => response === "")) {
      setError(
        "Responda completamente todas las preguntas antes de enviar el cuestionario."
      );
      return;
    }

    const payload = questions.map((question, index) => ({
      question,
      answer: responses[index],
    }));

    try {
      const response = await submitQuestionnaire(parsedDiagnosticId, payload);
      console.log("Formulario enviado:", response);
      setError("");
    } catch (error) {
      console.error("Error al enviar el cuestionario:", error);
      setError(
        "Error al enviar el cuestionario. Inténtelo de nuevo más tarde."
      );
    }
  };

  console.log("Diagnostic ID received:", diagnosticId);

  if (!diagnosticId) {
    return <div>Error: Diagnostic ID not found.</div>;
  }

  return (
    <div className={styles.questionnaireContainer}>
      <h1 className={styles.titleQuestionnaire}>Cuestionario</h1>
      {questions.map((question, index) => (
        <div className={styles.questionsForm} key={index}>
          <div className={styles.questionContainer}>
            <p>{question}</p>
            <div className={styles.optionsContainer}>
              {answers.map((answer, ansIndex) => (
                <label key={ansIndex} className={styles.optionLabel}>
                  <input
                    type="radio"
                    name={`question-${index}`}
                    value={answer}
                    checked={responses[index] === answer}
                    onChange={() => handleResponseChange(index, answer)}
                  />
                  <span className={styles.radioCustom}></span>
                  {answer}
                </label>
              ))}
            </div>
          </div>
        </div>
      ))}
      {error && <p className={styles.errorMessage}>{error}</p>}
      <button className={styles.btnQuestionnaire} onClick={handleSubmit}>
        Enviar Cuestionario
      </button>
    </div>
  );
};

export default Questionnaire;
