import { useState } from "react";

const initialForm = {
  area: "",
  bedrooms: "",
  bathrooms: "",
  parking: "",
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "https://ai-house-price-prediction-zj1l.onrender.com/api/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(form),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Prediction failed");
      }

      if (!data.success) {
        throw new Error(data.error || "Prediction failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app">
      <section className="hero">
        <h1>House Price Prediction</h1>
        <p>
          Enter property details and get an estimated house price.
        </p>
      </section>

      <section className="card">
        <form onSubmit={handleSubmit}>
          <div className="grid">
            <Input
              label="Area (sq. ft.)"
              name="area"
              value={form.area}
              onChange={handleChange}
              min="1"
            />

            <Input
              label="Bedrooms"
              name="bedrooms"
              value={form.bedrooms}
              onChange={handleChange}
              min="1"
            />

            <Input
              label="Bathrooms"
              name="bathrooms"
              value={form.bathrooms}
              onChange={handleChange}
              min="1"
            />

            <Input
              label="Parking Spaces"
              name="parking"
              value={form.parking}
              onChange={handleChange}
              min="0"
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Predict House Price"}
          </button>
        </form>

        {error && <div className="error">⚠️ {error}</div>}

        {result && (
          <div className="result">
            <p>Estimated House Price</p>

            <h2>{result.formatted_price}</h2>

            <span>
              Prediction generated using a Random Forest ML model.
            </span>
          </div>
        )}
      </section>
    </main>
  );
}

function Input({ label, name, value, onChange, min }) {
  return (
    <label>
      <span>{label}</span>

      <input
        type="number"
        name={name}
        value={value}
        onChange={onChange}
        min={min}
        required
      />
    </label>
  );
}

export default App;