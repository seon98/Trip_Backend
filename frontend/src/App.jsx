import { Route, Routes } from 'react-router-dom';
import Footer from './components/Footer';
import Header from './components/Header';
import HomePage from './pages/HomePage';
// LoginPage와 RegisterPage는 다음 단계에서 추가하겠습니다.
// import LoginPage from './pages/LoginPage';
// import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <main className="py-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* <Route path="/login" element={<LoginPage />} /> */}
          {/* <Route path="/register" element={<RegisterPage />} /> */}
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
