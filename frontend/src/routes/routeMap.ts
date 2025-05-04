import Dashboard from '@/components/content/dashboard/Dashboard'
import ImageViewer from '@/components/content/theme/colors/ImageViewer'
import Typography from '@/components/content/theme/typography/Typography'

export type RouteEntry = {
    path: string,
    name: string,
    element: React.FC,
    exact?: boolean,
}

const routeMap: Record<string, RouteEntry> = {
  Dashboard: { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  ImageViewer: { path: '/theme/ImageViewer', name: 'Theme', element: ImageViewer },
  Typography: { path: '/theme/typography', name: 'Typography', element: Typography },
}

export default routeMap
