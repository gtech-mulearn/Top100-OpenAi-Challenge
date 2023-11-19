import React from 'react'
import NavBar from '../components/NavBar'
import { Link } from "react-router-dom";
function Home() {
  return (
    <main>
      <NavBar />
      <section className="hero">
  
        <h1>Med reports</h1>
          <Link to="/report"> <button>Create report</button></Link>
      </section>
    </main>
  );
}

export default Home
