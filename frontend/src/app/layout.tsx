import './globals.css'
import type { Metadata } from 'next'
import StoreProvider from '@/store/StoreProvider'

import AppSidebar from '@/components/AppSidebar'
import AppHeader from '@/components/AppHeader'
// import AppContent from '@/components/AppContent'
// import AppFooter from '@/components/AppFooter'

export const metadata: Metadata = {
  title: 'My Electron Next App',
  description: 'Modern frontend for WSI viewer',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <StoreProvider>
          <div>
            <AppSidebar />
            <div className="wrapper d-flex flex-column min-vh-100">
              <AppHeader />
              <div className="body flex-grow-1">
                {children}
              </div>
              {/* <AppFooter /> */}
            </div>
          </div>
        </StoreProvider>
      </body>
    </html>
  )
}