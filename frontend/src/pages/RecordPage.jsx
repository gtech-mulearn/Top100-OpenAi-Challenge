import React from 'react'
import Recorder from '../components/Recorder'
import NavBar from '../components/NavBar'

function RecordPage() {
  return (
    <main>
      <NavBar />
      <div className="micwave-container">
      <Recorder />
      </div>
    </main>
  );
}

export default RecordPage;
