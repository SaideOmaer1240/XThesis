import React from "react";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Container";
import Rewrite from "./pages/RewriteJob";
import LandingPage from "./pages/LandingPage";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import TopicList from "./pages/TopicList";
import Thesis from "./pages/Thesis";
import Plan from "./components/plan";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />

        <Route
          path="/rewrite"
          element={
            <ProtectedRoute>
              <Rewrite />
            </ProtectedRoute>
          }
        />

        <Route
          path="/workspace"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        <Route
          path="/topic"
          element={
            <ProtectedRoute>
              <TopicList />
            </ProtectedRoute>
          }
        />
        <Route 
         path="/plan"
         element={
          <ProtectedRoute>
            <Plan/>
          </ProtectedRoute>
         }
        />

        <Route
          path="/thesis/:topicName"
          element={
            <ProtectedRoute>
              <Thesis />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
