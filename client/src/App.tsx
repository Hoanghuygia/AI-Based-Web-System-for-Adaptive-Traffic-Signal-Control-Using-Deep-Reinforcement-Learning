

import React from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { store } from './stores';

const TestPage: React.FC = () => {
  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh', 
      fontSize: '24px',
      backgroundColor: '#f0f0f0'
    }}>
      Test Page Works!
    </div>
  );
};

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<TestPage />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  );
}

// export default App;
