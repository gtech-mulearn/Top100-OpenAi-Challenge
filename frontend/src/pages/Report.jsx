import React from 'react'
import Recorder from '../components/Recorder'
import NavBar from '../components/NavBar'

function Report() {
  return (
    <main>
      <NavBar />
      <div className="micwave-container">
      <Recorder />
      </div>
    </main>
  );
}

export default Report
