export const createSSEConnection = (
  url: string,
  options: {
    method?: string
    headers?: Record<string, string>
    body?: any
    onMessage: (event: string, data: any) => void
    onError?: (error: Error) => void
    onComplete?: () => void
  }
): (() => void) => {
  let aborted = false

  const abort = () => {
    aborted = true
  }

  ;(async () => {
    try {
      const response = await fetch(url, {
        method: options.method || 'POST',
        headers: options.headers || {},
        body: options.body ? JSON.stringify(options.body) : undefined,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) {
        throw new Error('Unable to read response stream')
      }

      let buffer = ''

      while (!aborted) {
        const { done, value } = await reader.read()

        if (done) {
          options.onComplete?.()
          break
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        let currentEvent = ''
        let currentData = ''

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.substring(7).trim()
          } else if (line.startsWith('data: ')) {
            currentData = line.substring(6).trim()

            if (currentEvent && currentData) {
              try {
                const parsed = JSON.parse(currentData)
                options.onMessage(currentEvent, parsed)
              } catch (e) {
                // Ignore parsing errors
              }

              currentEvent = ''
              currentData = ''
            }
          }
        }
      }
    } catch (error) {
      if (!aborted) {
        options.onError?.(error as Error)
      }
    }
  })()

  return abort
}
