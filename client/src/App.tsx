import React from 'react';
import { Provider, useSelector } from 'react-redux';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { store, RootState } from './stores';

import { Typography, Button, Alert } from 'antd';

const { Title, Text } = Typography;

export type Locale = 'en_US' | 'vi_VN';

const queryClient = new QueryClient();

// const TestPage: React.FC = () => {
//   return (
//     <div
//       style={{
//         display: 'flex',
//         justifyContent: 'center',
//         alignItems: 'center',
//         height: '100vh',
//         fontSize: '24px',
//         backgroundColor: '#f00000',
//       }}
//     >
//       Test Page Works!
//     </div>
//   );
// };


const TestPage: React.FC = () => {
  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      height: '100vh', 
      gap: '20px', 
      padding: '20px' 
    }}>
      <Title level={2}>Ant Design Test Page</Title>
      <Text type="secondary">This is a test to verify Ant Design is working correctly</Text>
      <Button type="primary">Click Me</Button>
      <Alert 
        message="Ant Design Component Loaded Successfully" 
        type="success" 
        showIcon 
      />
    </div>
  );
};

const AppContent: React.FC = () => {
  const locale = useSelector((state: RootState) => state.user.locale);

  const getAntdLocale = () => {
    if (locale === 'en_US') {
      return enUS;
    } else {
      return viVN;
    }
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<TestPage />} />
      </Routes>
    </BrowserRouter>
  );
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Provider store={store}>
        <AppContent />
      </Provider>
    </QueryClientProvider>
  );
}

export default App;

// import './App.css';
// import { QueryClient, QueryClientProvider } from 'react-query';
// import { BrowserRouter, Routes, Route } from 'react-router-dom';
// import { Provider, useSelector } from 'react-redux';
// import { store, RootState } from './stores';
// import { ConfigProvider } from 'antd';
// // import enUS from 'antd/es/calendar/locale/en_US';
// import enUS from 'antd/es/locale/en_US';
// import viVN from 'antd/es/locale/vi_VN';
// import { IntlProvider } from 'react-intl';
// import { localeConfig } from './locale';
// import RenderRouter from './router';
// import React from 'react';

// const TestPage: React.FC = () => {
//   return (
//     <div
//       style={{
//         display: 'flex',
//         justifyContent: 'center',
//         alignItems: 'center',
//         height: '100vh',
//         fontSize: '24px',
//         backgroundColor: '#f0f0f0',
//       }}
//     >
//       Test Page Works!
//     </div>
//   );
// };

// export type Locale = 'en_US' | 'vi_VN';

// const queryClient = new QueryClient();

// function App() {
//   const locale = useSelector((state: RootState) => state.user.locale);

//   const getAntdLocale = () => {
//     if (locale === 'en_US') {
//       return enUS;
//     } else {
//       return viVN;
//     }
//   };

//   return (
//     <Provider store={store}>
//       <QueryClientProvider client={queryClient}>
//         <ConfigProvider locale={getAntdLocale()} componentSize="middle">
//           <IntlProvider
//             locale={locale.split('_')[0]}
//             messages={localeConfig[locale]}
//           >
//             <BrowserRouter>
//               <Routes>
//                 <Route path="/" element={<TestPage />} />
//               </Routes>
//               // <RenderRouter />
//             </BrowserRouter>
//           </IntlProvider>
//         </ConfigProvider>
//       </QueryClientProvider>
//     </Provider>
//   );
// }

// export default App;
