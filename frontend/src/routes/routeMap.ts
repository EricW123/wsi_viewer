import Dashboard from '@/components/content/dashboard/Dashboard'
import ImageViewer from '@/components/content/theme/colors/ImageViewer'
import Typography from '@/components/content/theme/typography/Typography'

const routeMap: Record<string, React.FC> = {
  Dashboard: Dashboard,
  ImageViewer: ImageViewer,
  Typography: Typography,
}

export default routeMap
