import React, { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import * as d3 from "d3";
import styles from "../styles/Results.module.css";
import { getAutismScore } from "../services/api";

interface Hospital {
  name: string;
  phone: string;
  address: string;
}

const Results: React.FC = () => {
  const { diagnosticId } = useParams<{ diagnosticId: string }>();
  const chartRef = useRef<SVGSVGElement>(null);
  const [teaPercentage, setTeaPercentage] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const hospitals: Hospital[] = [
    {
      name: "Hospital José Carrasco Arteaga (IESS)",
      phone: "(07) 286-1500",
      address:
        "https://www.google.com/maps/dir//Jos%C3%A9+Carrasco+Arteaga+entre+Popay%C3%A1n+y+Pacto+Andino,+Camino+A+Rayoloma,+Cuenca/@-2.898695,-79.05252,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x91cd19cb8d7c0869:0xb22d207c8625e97b!2m2!1d-78.970118!2d-2.898698?entry=ttu",
    },
    {
      name: "Hospital de Niños Dr. Roberto Gilbert E.",
      phone: "(04) 228-7310",
      address:
        "https://www.google.com/maps/dir//Av.+Roberto+Gilbert+y,+Sufragio+Libre,+Guayaquil+090514/@-2.1776452,-79.9659653,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x902d6dcf09098fd3:0xeef237e0ffeb9258!2m2!1d-79.8835633!2d-2.1776474?entry=ttu",
    },
    {
      name: "Hospital Pediátrico Baca Ortiz",
      phone: "(02) 394-2800",
      address:
        "https://www.google.com/maps/dir/-0.9676533,-80.7089101/Hospital+Pedi%C3%A1trico+Baca+Ortiz/@-0.5987503,-80.9160023,8z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5!1m1!1s0x91d59a0d5dd765c3:0x472e64a29c03bf9d!2m2!1d-78.486101!2d-0.2028697?entry=ttu",
    },
    {
      name: "Instituto de Neurociencias",
      phone: "(04) 256-0300",
      address:
        "https://www.google.com/maps?gs_lcrp=EgZjaHJvbWUqCQgAEEUYOxiABDIJCAAQRRg7GIAEMgcIARAAGIAEMggIAhAAGBYYHjIICAMQABgWGB4yCggEEAAYgAQYogQyCggFEAAYgAQYogTSAQc3NTJqMGoxqAIAsAIA&um=1&ie=UTF-8&fb=1&gl=ec&sa=X&geocode=KZeurofObS2QMZyb8I8hpS0Y&daddr=R4FC%2B34J,+Av.+Pedro+Men%C3%A9ndez+Gilbert,+Guayaquil+090514",
    },
  ];

  useEffect(() => {
    const fetchResults = async () => {
      if (!diagnosticId) {
        setError("No se encontró el ID del diagnóstico");
        return;
      }

      try {
        const autismScore = await getAutismScore(parseInt(diagnosticId));
        setTeaPercentage(Math.round(autismScore * 100));
      } catch (error) {
        console.error("Error fetching results:", error);
        setError(
          "Error al obtener los resultados. Por favor, intente de nuevo más tarde."
        );
      }
    };

    fetchResults();
  }, [diagnosticId]);

  useEffect(() => {
    if (chartRef.current && teaPercentage !== null) {
      drawChart();
    }
  }, [teaPercentage]);

  const drawChart = () => {
    const svg = d3.select(chartRef.current);
    svg.selectAll("*").remove();

    const width = 300;
    const height = 300;
    const margin = 40;
    const radius = Math.min(width, height) / 2 - margin;

    svg.attr("width", width).attr("height", height);

    const g = svg
      .append("g")
      .attr("transform", `translate(${width / 2},${height / 2})`);

    const gradient = svg
      .append("defs")
      .append("radialGradient")
      .attr("id", "gaugeGradient");

    gradient.append("stop").attr("offset", "0%").attr("stop-color", "#ff9ff3");

    gradient
      .append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "#d58cfc");

    const backgroundArc = d3
      .arc()
      .innerRadius(radius * 0.65)
      .outerRadius(radius)
      .startAngle(0)
      .endAngle(2 * Math.PI);

    g.append("path")
      .attr("class", styles.chartBackground)
      .attr("d", backgroundArc as any);

    const valueArc = d3
      .arc()
      .innerRadius(radius * 0.65)
      .outerRadius(radius)
      .startAngle(0)
      .endAngle((teaPercentage / 100) * 2 * Math.PI);

    g.append("path")
      .attr("class", styles.chartFill)
      .attr("d", valueArc as any)
      .style("fill", "url(#gaugeGradient)");

    g.append("text")
      .attr("class", styles.chartText)
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .text(`${teaPercentage}%`);

    const glowFilter = svg.append("defs").append("filter").attr("id", "glow");

    glowFilter
      .append("feGaussianBlur")
      .attr("stdDeviation", "3.5")
      .attr("result", "coloredBlur");

    const feMerge = glowFilter.append("feMerge");
    feMerge.append("feMergeNode").attr("in", "coloredBlur");
    feMerge.append("feMergeNode").attr("in", "SourceGraphic");

    g.select(".chartFill").style("filter", "url(#glow)");
  };

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (teaPercentage === null) {
    return <div className={styles.loading}>Cargando resultados...</div>;
  }

  return (
    <div className={styles.scrollContainer}>
      <div className={styles.resultsContainer}>
        <h1 className={styles.titleResults}>Resultados</h1>
        <div className={styles.chartContainer}>
          <svg ref={chartRef}></svg>
        </div>
        <p>El porcentaje estimado de TEA es: {teaPercentage}%</p>
        <h2>Hospitales</h2>
        <p>
          Aquí se detalla información de contacto y dirección de hospitales
          capacitados para realizar un verdadero análisis para determinar si el
          infante tiene TEA
        </p>
        <div className={styles.hospitalGrid}>
          {hospitals.map((hospital, index) => (
            <div key={index} className={styles.hospitalCard}>
              <h3>{hospital.name}</h3>
              <p>Teléfono: {hospital.phone}</p>
              <p>
                <a
                  href={hospital.address}
                  className={styles.howGo}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  ¿Cómo llegar?
                </a>
              </p>
            </div>
          ))}
        </div>
        <div className={styles.buttonContainer}>
          <a href="/" className={styles.buttons}>
            Volver al inicio
          </a>
          <a href="/scan" className={styles.buttons}>
            Realizar otro diagnostico
          </a>
        </div>
      </div>
    </div>
  );
};

export default Results;
