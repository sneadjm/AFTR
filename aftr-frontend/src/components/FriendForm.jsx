import { useState } from "react";
import API from "../api/axios";

export default function FriendForm({ onCreated }) {
  const [name, setName] = useState("");
  const [birthday, setBirthday] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("/friends/", {
        name,
        birthday,
      });
      setName("");
      setBirthday("");
      onCreated?.(res.data); // notify parent to refresh
    } catch (err) {
      console.error("Failed to create friend:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded mb-6">
      <h2 className="text-lg font-semibold">➕ Add a New Friend</h2>
      <input
        type="text"
        placeholder="Friend's Name"
        className="border w-full p-2"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="date"
        className="border w-full p-2"
        value={birthday}
        onChange={(e) => setBirthday(e.target.value)}
        required
      />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        Add Friend
      </button>
    </form>
  );
}
