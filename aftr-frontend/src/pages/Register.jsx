import { useState } from "react";
import API from "../api/axios";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const register = async (e) => {
    e.preventDefault();
    try {
      await API.post("/auth/register", { email, password });
      alert("Account created! You can now log in.");
      navigate("/");
    } catch (err) {
      console.error("Registration failed:", err);
      alert("Error: " + err?.response?.data?.detail || "Unknown error");
    }
  };

  return (
    <form onSubmit={register} className="max-w-md mx-auto mt-10 space-y-4">
      <h1 className="text-2xl font-bold">Create an Account</h1>
      <input
        type="email"
        placeholder="Email"
        className="border w-full p-2"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        className="border w-full p-2"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit" className="bg-green-600 text-white px-4 py-2">
        Register
      </button>

      <p className="text-sm">
        Already have an account?{" "}
        <Link to="/" className="text-blue-600 underline">
          Log in
        </Link>
      </p>
    </form>
  );
}
