import React, { useState, useEffect } from 'react'
function Login() {
  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/members").then(
      res => res.json()
      
  ).then(
    data => {
      setData(data)
      console.log(data)
    }
  )
}, [])
  return (
    <div className="Login">
      {(typeof data.members === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        data.members.map((member, i) => (
          <p key={i}>{member}</p>
        ))
      )}
    </div>
  );
}
export default Login;
