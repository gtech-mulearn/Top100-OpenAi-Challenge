import './App.css'
import Upload from './pages/Upload'
import Chat from './pages/Chat'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Mail } from 'lucide-react';
import { MainApp } from './pages/MainApp';
import { DetailsPage } from './pages/DetailsPage';

function App() {

  return (
    <>
      <Router>
          <Routes>
              <Route path="/" element={<MainApp/>} />
              <Route path="/detailspage" element={<DetailsPage/>} />
          </Routes>
      </Router>
    </>
  )
}

export default App