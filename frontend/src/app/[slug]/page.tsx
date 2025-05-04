'use client'

import { useParams } from 'next/navigation'
import routeMap from '@/routes/routeMap'

export default function DynamicPage() {
  const { slug } = useParams()
  const route = routeMap[slug as string] || routeMap['Dashboard'] // Fallback to Dashboard if slug is not found

  const PageComponent = route.element
  if (!PageComponent) {
    return <div>404: Page not found</div>
  }

  return <PageComponent />
}
