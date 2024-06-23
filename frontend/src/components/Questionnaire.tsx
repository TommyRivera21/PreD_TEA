import React, { useState } from 'react';
import styles from '../styles/Questionnaire.module.css';

const questions = [
  "Pregunta 1",
  "Pregunta 2",
  "Pregunta 3",
  // Agrega más preguntas aquí
];

const Questionnaire: React.FC = () => {
  const [responses, setResponses] = useState<string[]>(Array(questions.length).fill(''));

  const handleResponseChange = (index: number, value: string) => {
    const newResponses = [...responses];
    newResponses[index] = value;
    setResponses(newResponses);
  };

  const handleSubmit = () => {
    // Lógica para enviar las respuestas al backend
    console.log(responses);
  };

  return (
    <div className={styles.questionnaire}>
      <h1>Cuestionario</h1>
      {questions.map((question, index) => (
        <div key={index}>
          <p>{question}</p>
          <input
            type="text"
            value={responses[index]}
            onChange={(e) => handleResponseChange(index, e.target.value)}
          />
        </div>
      ))}
      <button onClick={handleSubmit}>Enviar</button>
    </div>
  );
};

export default Questionnaire;
