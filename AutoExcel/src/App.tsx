import './App.css'
import Upload from './pages/Upload'
import Chat from './pages/Chat'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {

  return (
    <>
      <Router>
          <Routes>
              <Route path="/" element={<Upload />} />
              <Route path="/chat" element={<Chat />} />
          </Routes>
      </Router>
    </>
  )
}

export default App