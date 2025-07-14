import { useEffect, useState } from "react";
import API from "../api/axios";
import FriendForm from "../components/FriendForm";

export default function Dashboard() {
  const [friends, setFriends] = useState([]);

  const fetchFriends = async () => {
    const res = await API.get("/friends");
    setFriends(res.data);
  };

  useEffect(() => {
    fetchFriends();
  }, []);

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">🎂 Your Friends</h1>

      <FriendForm onCreated={fetchFriends} />

      <ul className="space-y-2">
        {friends.map((f) => (
          <li key={f.id} className="border p-2 rounded">
            <span className="font-semibold">{f.name}</span> — {f.birthday}
          </li>
        ))}
      </ul>
    </div>
  );
}
