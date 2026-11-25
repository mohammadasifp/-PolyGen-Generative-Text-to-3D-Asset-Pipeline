
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const generateModel = async (prompt) => {
  const response = await API.post("/api/generate", {
    prompt: prompt,
  });

  return response.data;
};

export default API;
