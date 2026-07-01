import { Routes, Route, Navigate } from "react-router-dom";
import ResumeOptimizer from "./pages/ResumeOptimizer";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import UploadResume from "./pages/UploadResume";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import ATSScore from "./pages/ATSScore";
import JobAnalyzer from "./pages/JobAnalyzer";
import ColdEmail from "./pages/ColdEmail";
import Pipeline from "./pages/Pipeline";
import LandingPage from "./pages/LandingPage";
function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />

      <Route path="/login" element={<Login />} />

      <Route path="/register" element={<Register />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
    path="/resume"
    element={
        <ProtectedRoute>
            <UploadResume />
        </ProtectedRoute>
    }
/>
<Route
    path="/ats"
    element={
        <ProtectedRoute>
            <ATSScore/>
        </ProtectedRoute>
    }
/>
<Route
  path="/optimizer"
  element={
    <ProtectedRoute>
      <ResumeOptimizer />
    </ProtectedRoute>
  }
/>
<Route
  path="/analyze"
  element={
    <ProtectedRoute>
      <JobAnalyzer />
    </ProtectedRoute>
  }
/>
<Route
  path="/email"
  element={
    <ProtectedRoute>
      <ColdEmail />
    </ProtectedRoute>
  }
/>
<Route
  path="/pipeline"
  element={
    <ProtectedRoute>
      <Pipeline />
    </ProtectedRoute>
  }
/>
    </Routes>
  );
}

export default App;