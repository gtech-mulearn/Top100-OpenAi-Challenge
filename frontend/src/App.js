import './App.css';
import { Route, Routes } from "react-router-dom";
import Home from './pages/Home';
import RecordPage from './pages/RecordPage';
import Reports from './pages/Reports';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/report" element={<RecordPage/>} />
      <Route path="/reports" element={<Reports />} />
    </Routes>
  );
}

export default App;
