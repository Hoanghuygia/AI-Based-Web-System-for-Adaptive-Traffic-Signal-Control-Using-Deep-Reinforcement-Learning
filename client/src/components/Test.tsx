// import { Button } from 'antd';

// export default function Test() {
//   return (
//     <>
//         <div className="App">
//             <Button type="primary">Button</Button>
//         </div>
//         <div className="text-color"> Huy abc</div> 
//         <span className='text-red-500'>TailwindCSs</span>
//     </>
//   )
// }

import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { login, logout } from '@src/stores/user.slice';
import { RootState, AppDispatch } from '@src/stores';
import { Button, Spin } from 'antd';

export default function Test() {
  const dispatch = useDispatch<AppDispatch>();
  const { currentUser, loading, error, token, refreshToken } = useSelector((state: RootState) => state.user);

  const handleLogin = () => {
    dispatch(login({
      username: 'diemquynh123456',
      password: 'diemquynh123456'
    }));
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <>
      <div className="p-4 space-y-4">
        <h2 className="text-xl font-semibold">Redux Test Component</h2>

        {loading && <Spin />}
        {error && <p className="text-red-500">Error: {error}</p>}
        {currentUser ? (
          <>
            <p className="text-green-600">Logged in as: {currentUser || 'Unknown User'}</p>
            <p>Token: {token}</p>
            <p>Refresh token: {refreshToken}</p>
            <Button type="primary" danger onClick={handleLogout}>Logout</Button>
          </>
        ) : (
          <>
            <p className="text-gray-600">Not logged in</p>
            <Button type="primary" onClick={handleLogin}>Login</Button>
          </>
        )}
      </div>
    </>
  );
}

