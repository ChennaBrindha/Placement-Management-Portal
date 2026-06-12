import { useState } from "react";
import axios from "axios";

function Login() {

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const login = async () => {

    const res =
      await axios.post(
      "http://localhost:5000/api/auth/login",
      {
        email,
        password
      });

    localStorage.setItem(
      "token",
      res.data.token
    );
  };

  return (
    <div>

      <h1>Login</h1>

      <input
       placeholder="Email"
       onChange={(e)=>
       setEmail(e.target.value)}
      />

      <input
       type="password"
       placeholder="Password"
       onChange={(e)=>
       setPassword(e.target.value)}
      />

      <button
      onClick={login}>
      Login
      </button>

    </div>
  );
}

export default Login;