import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Button } from './components/ui/button'
import { Calendar } from './components/ui/calendar'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Button variant="outline" className='hover:bg-white'>shadcn</Button>
    </>
  )
}

export default App
