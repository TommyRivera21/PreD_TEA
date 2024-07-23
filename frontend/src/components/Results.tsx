import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import styles from "../styles/Results.module.css";

interface Hospital {
  name: string;
  phone: string;
  address: string;
}

const Results: React.FC = () => {
  const chartRef = useRef<SVGSVGElement>(null);
  const teaPercentage = 47; 

  const hospitals: Hospital[] = [
    { name: "Hospital A", phone: "123-456-7890", address: "Calle 1, Ciudad" },
    { name: "Hospital B", phone: "234-567-8901", address: "Calle 2, Ciudad" },
    { name: "Hospital C", phone: "345-678-9012", address: "Calle 3, Ciudad" },
    { name: "Hospital D", phone: "456-789-0123", address: "Calle 4, Ciudad" },
  ];

  useEffect(() => {
    if (chartRef.current) {
      drawChart();
    }
  }, []);

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

    // Crear un gradiente radial
    const gradient = svg.append("defs")
      .append("radialGradient")
      .attr("id", "gaugeGradient");

    gradient.append("stop")
      .attr("offset", "0%")
      .attr("stop-color", "#ff9ff3");

    gradient.append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "#d58cfc");

    // Fondo del gauge
    const backgroundArc = d3.arc()
      .innerRadius(radius * 0.65)
      .outerRadius(radius)
      .startAngle(0)
      .endAngle(2 * Math.PI);

    g.append("path")
      .attr("class", styles.chartBackground)
      .attr("d", backgroundArc as any);

    // Arco del valor
    const valueArc = d3.arc()
      .innerRadius(radius * 0.65)
      .outerRadius(radius)
      .startAngle(0)
      .endAngle((teaPercentage / 100) * 2 * Math.PI);

    g.append("path")
      .attr("class", styles.chartFill)
      .attr("d", valueArc as any)
      .style("fill", "url(#gaugeGradient)");

    // Texto central
    g.append("text")
      .attr("class", styles.chartText)
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .text(`${teaPercentage}%`);

    // Agregar un efecto de brillo
    const glowFilter = svg.append("defs")
      .append("filter")
      .attr("id", "glow");

    glowFilter.append("feGaussianBlur")
      .attr("stdDeviation", "3.5")
      .attr("result", "coloredBlur");

    const feMerge = glowFilter.append("feMerge");
    feMerge.append("feMergeNode")
      .attr("in", "coloredBlur");
    feMerge.append("feMergeNode")
      .attr("in", "SourceGraphic");

    g.select(".chartFill")
      .style("filter", "url(#glow)");
  };

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
          capacitados para realizar un verdadero análisis para determinar si el infante tiene TEA
        </p>
        <div className={styles.hospitalGrid}>
          {hospitals.map((hospital, index) => (
            <div key={index} className={styles.hospitalCard}>
              <h3>{hospital.name}</h3>
              <p>Teléfono: {hospital.phone}</p>
              <p>Dirección: {hospital.address}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Results;