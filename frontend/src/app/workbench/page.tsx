'use client'

import { useCallback, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icons } from '@/components/ui/icons'
import { cn } from '@/lib/utils'
import { apiClient } from '@/lib/api-client'
import { useAI } from '@/context/AIContext'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
}

interface ReviewItem {
  id: string
  campaign: string
  issue: string
  status: string
  severity?: 'high' | 'medium' | 'low'
  agent?: string
}

// Sample workbench tools
const tools = [
  {
    id: 'ai-assistant',
    title: 'AI Assistant',
    description: 'Chat with your AI assistant for help with tasks',
    icon: Icons.sparkles,
    color: 'bg-gradient-to-br from-brand-navy to-brand-purple',
    status: 'available',
  },
  {
    id: 'automation',
    title: 'Automation Builder',
    description: 'Create and manage automated workflows',
    icon: Icons.zap,
    color: 'bg-gradient-to-br from-brand-cornflower to-brand-purple',
    status: 'available',
  },
  {
    id: 'analytics',
    title: 'Analytics Dashboard',
    description: 'View detailed analytics and reports',
    icon: Icons.activity,
    color: 'bg-gradient-to-br from-emerald-500 to-emerald-600',
    status: 'available',
  },
  {
    id: 'integrations',
    title: 'Integrations',
    description: 'Connect with third-party services',
    icon: Icons.share,
    color: 'bg-gradient-to-br from-amber-500 to-orange-500',
    status: 'available',
  },
]

function ToolCard({
  tool,
  onOpen,
}: {
  tool: (typeof tools)[0]
  onOpen: (toolId: string) => void
}) {
  const Icon = tool.icon
  const isComingSoon = tool.status === 'coming-soon'

  return (
    <motion.div variants={itemVariants}>
      <Card
        className={cn(
          'h-full cursor-pointer transition-all duration-300',
          isComingSoon && 'opacity-60'
        )}
      >
        <CardHeader>
          <div className='flex items-start justify-between'>
            <div
              className={cn(
                'flex h-12 w-12 items-center justify-center rounded-xl text-white',
                tool.color
              )}
            >
              <Icon className='h-6 w-6' strokeWidth={1.5} />
            </div>
            {isComingSoon && (
              <span className='rounded-full bg-muted px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-brand-muted'>
                Coming Soon
              </span>
            )}
          </div>
          <CardTitle className='mt-4'>{tool.title}</CardTitle>
          <CardDescription>{tool.description}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button
            variant={isComingSoon ? 'outline' : 'default'}
            className='w-full'
            disabled={isComingSoon}
            onClick={() => onOpen(tool.id)}
          >
            {isComingSoon ? 'Notify Me' : 'Open Tool'}
            {!isComingSoon && <Icons.arrowRight className='ml-2 h-4 w-4' />}
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default function WorkbenchPage() {
  const router = useRouter()
  const { openManager, addMessage } = useAI()
  const [reviews, setReviews] = useState<ReviewItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [approvingId, setApprovingId] = useState<string | null>(null)
  const [actionMessage, setActionMessage] = useState('Workbench is ready.')

  const loadReviews = useCallback(async () => {
    setIsLoading(true)
    try {
      const data = await apiClient.get<{ reviews: ReviewItem[] }>('/api/workbench/reviews')
      setReviews(data.reviews)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    loadReviews()
  }, [loadReviews])

  const approveReview = useCallback(async (reviewId: string) => {
    setApprovingId(reviewId)
    try {
      await apiClient.post(`/api/workbench/approve?review_id=${encodeURIComponent(reviewId)}`)
      setReviews((current) =>
        current.map((review) =>
          review.id === reviewId
            ? { ...review, status: 'Approved' }
            : review
        )
      )
    } finally {
      setApprovingId(null)
    }
  }, [])

  const handleOpenTool = useCallback((toolId: string) => {
    if (toolId === 'ai-assistant') {
      openManager()
      addMessage({
        role: 'assistant',
        content: 'Workbench context loaded. Ask me to run a sales marketing campaign, show policy violations, or summarize approvals.',
      })
      setActionMessage('AI Assistant opened with Workbench context.')
      return
    }

    if (toolId === 'automation') {
      document.getElementById('human-review-queue')?.scrollIntoView({ behavior: 'smooth' })
      setActionMessage('Automation Builder loaded the current approval workflow.')
      return
    }

    if (toolId === 'analytics') {
      router.push('/ai/insights')
      return
    }

    if (toolId === 'integrations') {
      router.push('/settings')
    }
  }, [addMessage, openManager, router])

  const createTask = useCallback(() => {
    setReviews((current) => [
      {
        id: `review-${Date.now()}`,
        campaign: 'Sales Marketing',
        issue: 'New manual task created from Workbench quick action',
        status: 'Awaiting Approval',
        severity: 'medium',
        agent: 'Automation Builder',
      },
      ...current,
    ])
    setActionMessage('New review task created for Sales Marketing.')
  }, [])

  const generateReport = useCallback(async () => {
    const data = await apiClient.get<{
      roi: string
      engagement: string
      violations_prevented: number
      campaigns_reviewed: number
    }>('/api/insights')
    setActionMessage(
      `Report generated: ROI ${data.roi}, engagement ${data.engagement}, ${data.violations_prevented} violations prevented.`
    )
  }, [])

  const sendNotification = useCallback(() => {
    setActionMessage('Notification sent to campaign owner and Brand Safety reviewer.')
  }, [])

  const exportData = useCallback(() => {
    const payload = {
      exported_at: new Date().toISOString(),
      reviews,
    }
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'workbench-export.json'
    link.click()
    URL.revokeObjectURL(url)
    setActionMessage('Workbench export downloaded.')
  }, [reviews])

  return (
    <motion.div
      className='space-y-8'
      variants={containerVariants}
      initial='hidden'
      animate='visible'
    >
      {/* Header */}
      <motion.div variants={itemVariants}>
        <h1 className='text-display-3 font-bold tracking-tight text-brand-navy'>
          Workbench
        </h1>
        <p className='mt-2 text-lg text-muted-foreground'>
          Access your AI tools and automation workflows.
        </p>
      </motion.div>

      {/* Tools Grid */}
      <div className='grid gap-6 sm:grid-cols-2 lg:grid-cols-4'>
        {tools.map((tool) => (
          <ToolCard key={tool.id} tool={tool} onOpen={handleOpenTool} />
        ))}
      </div>

      <motion.div variants={itemVariants}>
        <Card>
          <CardContent className='flex items-center gap-3 py-4'>
            <div className='flex h-9 w-9 items-center justify-center rounded-lg bg-brand-cornflower/10'>
              <Icons.checkCircle className='h-5 w-5 text-brand-cornflower' />
            </div>
            <p className='text-sm font-medium text-brand-navy'>{actionMessage}</p>
          </CardContent>
        </Card>
      </motion.div>

      {/* Human Review Queue */}
      <motion.div variants={itemVariants} id='human-review-queue'>
        <Card>
          <CardHeader>
            <div className='flex items-center justify-between gap-4'>
              <div>
                <CardTitle className='flex items-center gap-2'>
                  <Icons.workbench className='h-5 w-5 text-brand-cornflower' />
                  Human Review Queue
                </CardTitle>
                <CardDescription>
                  Governance pauses that need approval before publishing.
                </CardDescription>
              </div>
              <Button variant='outline' size='sm' onClick={loadReviews} disabled={isLoading}>
                {isLoading ? (
                  <Icons.loader className='mr-2 h-4 w-4 animate-spin' />
                ) : (
                  <Icons.refresh className='mr-2 h-4 w-4' />
                )}
                Refresh
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className='flex items-center justify-center py-10'>
                <Icons.loader className='h-6 w-6 animate-spin text-brand-cornflower' />
              </div>
            ) : (
              <div className='space-y-3'>
                {reviews.map((review) => {
                  const isApproved = review.status === 'Approved'

                  return (
                    <div
                      key={review.id}
                      className={cn(
                        'flex flex-col gap-4 rounded-xl border border-border bg-white p-4',
                        'sm:flex-row sm:items-center sm:justify-between'
                      )}
                    >
                      <div className='min-w-0'>
                        <div className='flex flex-wrap items-center gap-2'>
                          <p className='font-semibold text-brand-navy'>
                            {review.campaign}
                          </p>
                          <span
                            className={cn(
                              'rounded-full px-2 py-0.5 text-xs font-medium',
                              review.severity === 'high'
                                ? 'bg-red-100 text-red-700'
                                : 'bg-amber-100 text-amber-700'
                            )}
                          >
                            {review.severity || 'medium'}
                          </span>
                          <span className='rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground'>
                            {review.agent || 'Agent'}
                          </span>
                        </div>
                        <p className='mt-1 text-sm text-muted-foreground'>
                          {review.issue}
                        </p>
                        <p className='mt-2 text-xs font-medium text-brand-muted'>
                          Status: {review.status}
                        </p>
                      </div>
                      <Button
                        variant={isApproved ? 'outline' : 'gradient'}
                        disabled={isApproved || approvingId === review.id}
                        onClick={() => approveReview(review.id)}
                        className='sm:w-36'
                      >
                        {approvingId === review.id ? (
                          <Icons.loader className='mr-2 h-4 w-4 animate-spin' />
                        ) : isApproved ? (
                          <Icons.check className='mr-2 h-4 w-4' />
                        ) : (
                          <Icons.checkCircle className='mr-2 h-4 w-4' />
                        )}
                        {isApproved ? 'Approved' : 'Approve'}
                      </Button>
                    </div>
                  )
                })}
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div variants={itemVariants}>
        <Card>
          <CardHeader>
            <CardTitle className='flex items-center gap-2'>
              <Icons.zap className='h-5 w-5 text-brand-cornflower' />
              Quick Actions
            </CardTitle>
            <CardDescription>
              Frequently used actions for faster access
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className='flex flex-wrap gap-3'>
              <Button variant='outline' size='sm' onClick={createTask}>
                <Icons.plus className='mr-2 h-4 w-4' />
                New Task
              </Button>
              <Button variant='outline' size='sm' onClick={generateReport}>
                <Icons.fileText className='mr-2 h-4 w-4' />
                Generate Report
              </Button>
              <Button variant='outline' size='sm' onClick={sendNotification}>
                <Icons.mail className='mr-2 h-4 w-4' />
                Send Notification
              </Button>
              <Button variant='outline' size='sm' onClick={exportData}>
                <Icons.download className='mr-2 h-4 w-4' />
                Export Data
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  )
}
