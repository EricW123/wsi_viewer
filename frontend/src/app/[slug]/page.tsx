'use client'

import { useParams } from 'next/navigation'
import routeMap from '@/routes/routeMap'

export default function DynamicPage() {
  const { slug } = useParams()
  const PageComponent = routeMap[slug as string]

  if (!PageComponent) {
    return routeMap['Dashboard'] // Fallback to Dashboard if the slug is not found
  }

  return <PageComponent />
}
