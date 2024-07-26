import axios, { AxiosResponse } from "axios";
import { API_URL } from "../constants";
import { getCurrentToken, refreshToken } from "./authService";

// Interfaces para las respuestas de la API
interface DiagnosticResponse {
  id: number;
  diagnostic_type: "video" | "image";
}

interface UploadResponse {
  url: string;
}

interface QuestionnaireResponse {
  message: string;
  questionnaire_id: number;
}

// Interface para la respuesta de los resultados
interface ResultsResponse {
  result_id: number;
  autism_score: number;
}

const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      console.error("Server responded with an error:", error.response.data);
      throw new Error(error.response.data.message || "API error");
    } else if (error.request) {
      console.error("No response received:", error.request);
      throw new Error("No response received from server");
    }
  }
  console.error("Unexpected error:", error);
  throw new Error("Unexpected error occurred");
};

export const createDiagnostic = async (
  scanType: "video" | "image"
): Promise<DiagnosticResponse> => {
  try {
    const token = getCurrentToken();
    if (!token) throw new Error("No authentication token found");

    const makeRequest = async (authToken: string) => {
      return axios.post<DiagnosticResponse>(
        `${API_URL}/diagnostic/create`,
        { scanType },
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
    };

    try {
      const response: AxiosResponse<DiagnosticResponse> = await makeRequest(token);
      console.log("Diagnostic created successfully:", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        const newToken = await refreshToken();
        const response: AxiosResponse<DiagnosticResponse> = await makeRequest(newToken);
        console.log("Diagnostic created successfully after token refresh:", response.data);
        return response.data;
      }
      throw error;
    }
  } catch (error) {
    return handleApiError(error);
  }
};

export const uploadVideo = async (
  formData: FormData,
  diagnosticId: number
): Promise<UploadResponse> => {
  try {
    const token = getCurrentToken();
    if (!token) throw new Error("No authentication token found");

    formData.append("diagnostic_id", diagnosticId.toString());

    const makeRequest = async (authToken: string) => {
      return axios.post(`${API_URL}/upload/video`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${authToken}`,
        },
      });
    };

    try {
      const response: AxiosResponse<UploadResponse> = await makeRequest(token);
      console.log("Video uploaded successfully:", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        const newToken = await refreshToken();
        const response: AxiosResponse<UploadResponse> = await makeRequest(newToken);
        console.log("Video uploaded successfully after token refresh:", response.data);
        return response.data;
      }
      throw error;
    }
  } catch (error) {
    return handleApiError(error);
  }
};

export const uploadImages = async (
  formData: FormData,
  diagnosticId: number
): Promise<UploadResponse> => {
  try {
    const token = getCurrentToken();
    if (!token) throw new Error("No authentication token found");

    formData.append("diagnostic_id", diagnosticId.toString());

    const makeRequest = async (authToken: string) => {
      return axios.post(`${API_URL}/upload/image`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${authToken}`,
        },
      });
    };

    try {
      const response: AxiosResponse<UploadResponse> = await makeRequest(token);
      console.log("Images uploaded successfully:", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        const newToken = await refreshToken();
        const response: AxiosResponse<UploadResponse> = await makeRequest(newToken);
        console.log("Images uploaded successfully after token refresh:", response.data);
        return response.data;
      }
      throw error;
    }
  } catch (error) {
    return handleApiError(error);
  }
};

export const submitQuestionnaire = async (
  diagnosticId: number,
  responses: { question: string; answer: string }[]
): Promise<QuestionnaireResponse> => {
  try {
    const token = getCurrentToken();
    if (!token) throw new Error("No authentication token found");

    const requestData = {
      qa_pairs: responses,
      diagnostic_id: diagnosticId,
    };

    const makeRequest = async (authToken: string) => {
      return axios.post(`${API_URL}/questionnaire/submit`, requestData, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
    };

    try {
      const response: AxiosResponse<QuestionnaireResponse> = await makeRequest(token);
      console.log("Questionnaire submitted successfully:", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        const newToken = await refreshToken();
        const response: AxiosResponse<QuestionnaireResponse> = await makeRequest(newToken);
        console.log("Questionnaire submitted successfully after token refresh:", response.data);
        return response.data;
      }
      throw error;
    }
  } catch (error) {
    return handleApiError(error);
  }
};

export const getResults = async (diagnosticId: number): Promise<ResultsResponse> => {
  try {
    const token = getCurrentToken();
    if (!token) throw new Error("No authentication token found");

    const makeRequest = async (authToken: string) => {
      return axios.get<ResultsResponse>(`${API_URL}/results/${diagnosticId}`, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
    };

    try {
      const response: AxiosResponse<ResultsResponse> = await makeRequest(token);
      console.log("Results fetched successfully:", response.data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        const newToken = await refreshToken();
        const response: AxiosResponse<ResultsResponse> = await makeRequest(newToken);
        console.log("Results fetched successfully after token refresh:", response.data);
        return response.data;
      }
      throw error;
    }
  } catch (error) {
    return handleApiError(error);
  }
};
