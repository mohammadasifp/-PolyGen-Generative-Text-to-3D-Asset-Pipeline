
import { useState } from "react";
import { generateModel } from "./services/api";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Please enter a 3D model description.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data = await generateModel(prompt);
      setResult(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to generate model. Check your backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <nav className="navbar">
        <h2>Poly<span>Gen</span></h2>
        <span className="nav-label">AI 3D GENERATOR</span>
      </nav>

      <main className="container">
        <section className="hero">
          <p className="tagline">CREATE WITHOUT LIMITS</p>
          <h1>
            Turn your ideas into
            <span> 3D reality.</span>
          </h1>
          <p className="description">
            Describe anything you imagine.
            PolyGen transforms your text into 3D models.
          </p>
        </section>

        <section className="generator">
          <label>Describe your 3D model</label>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: A futuristic sports car with metallic blue paint..."
          />

          <button
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? "Generating..." : "Generate 3D Model →"}
          </button>

          {loading && <p className="status">Processing your request...</p>}
          {error && <p className="error">{error}</p>}

          {result && (
            <div className="result">
              <h3>Generation response</h3>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </section>

        <footer>
          © 2026 PolyGen · AI Powered 3D Generation
        </footer>
      </main>
    </div>
  );
}

export default App;
