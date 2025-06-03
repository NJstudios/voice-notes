// frontend/src/App.tsx
import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Summaries from './pages/Summaries';

export default function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link> | <Link to="/summaries">Summaries</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/summaries" element={<Summaries />} />
      </Routes>
    </BrowserRouter>
  );
}
