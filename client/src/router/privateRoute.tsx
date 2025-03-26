import React, { FC, useEffect, ReactElement } from 'react'
import { Navigate, NavigateProps } from 'react-router-dom'
import { useLocation } from 'react-router'
import { useSelector } from 'react-redux'
import { RootState } from '@src/stores'

interface PrivateRouteProps {
  element: ReactElement & { props?: { titleId?: string } }
}

const PrivateRoute: FC<PrivateRouteProps> = ({ element }) => {
  const location = useLocation()
  const logged = useSelector((state: RootState) => state.user.logged)

  useEffect(() => {
    document.title = element.props?.titleId || 'Default Title'
  }, [element])

  return logged ? (
    element
  ) : (
    <Navigate to={`/login?from=${encodeURIComponent(location.pathname)}`} replace />
    // <Navigate to={{ pathname: `/login${'?from=' + encodeURIComponent(location.pathname)}` }} replace />
  )
}

export default PrivateRoute