import { useState } from "react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";

const styles = {
  container: {
    backgroundColor: "#8a9b5a", 
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
    flexDirection: "column", 
  },
  circle: {
    backgroundColor: "#2e4a1f",
    borderRadius: "50%",
    width: 360,
    height: 360,
    padding: 30,
    boxShadow: "0 0 15px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    textAlign: "center",
    boxSizing: "border-box",
    color: "white",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
    marginTop: 35,
  },
  subtitle: {
    marginBottom: 10,
    fontWeight: "600",
  },
  input: {
    width: "90%",
    maxWidth: "300px",
    padding: 8,
    marginBottom: 10,
    borderRadius: 4,
    border: "none",
    backgroundColor: "#1e3a0f",
    color: "white",
    fontSize: "1rem",
  },
  inputLast: {
    marginBottom: 15,
  },
  button: {
    width: "60%",
    maxWidth: "300px",
    padding: 10,
    borderRadius: 4,
    border: "none",
    backgroundColor: "#4a7c23",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
    alignSelf: "center",
  },
  registerContainer: {
    marginTop: 20,
    backgroundColor: "#2e4a1f",
    padding: "15px 20px",
    borderRadius: 8,
    color: "white",
    textAlign: "center",
    width: 320,
  },
  registerText: {
    marginBottom: 10,
    fontWeight: "600",
  },
  registerLink: {
    color: "white",
    textDecoration: "underline",
    cursor: "pointer",
  },
};

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await API.post("/auth/login", {
        email: username, // backend expects email
        password,
      });
      console.log("Login success:", response.data);
      // TODO: Save token, redirect user, etc.
    } catch (err) {
      console.error("Login error:", err);
      setError(
        err.response?.data?.detail || "Unexpected error, please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.circle}>
        <h1 style={styles.title}>Are you A Friend That Remembers?</h1>

        <form onSubmit={handleSubmit}>
          <p style={styles.subtitle}>If so, let's catch up:</p>

          <input
            type="text"
            placeholder="Email"
            style={styles.input}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={loading}
            required
          />

          <input
            type="password"
            placeholder="Password"
            style={{ ...styles.input, ...styles.inputLast }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={loading}
            required
          />

          <button style={styles.button} type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Log In"}
          </button>

          {error && (
            <p style={{ color: "salmon", marginTop: 10, fontWeight: "600" }}>
              {error}
            </p>
          )}
        </form>
      </div>

      <div style={styles.registerContainer}>
        <p style={styles.registerText}>If not (yet!), it's nice to meet you:</p>
        <a href="/register" style={styles.registerLink}>
          Register here
        </a>
      </div>
    </div>
  );
}