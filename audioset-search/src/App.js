import './App.css';
import { useState, useEffect } from 'react'
import { ReactComponent as SeachSvg } from './search.svg'

function Search(){
  const [urlInput, setUrlInput] = useState('')
  // const [requestData, setRequestData] = useState({})
  const [responseData, setResponseData] = useState({})
  const [hasResult, setHasResult] = useState(false)
  
  const [randomVideo, setRandomVideo] = useState('')

  function handleChange(event) {
     const { value } = event.target
     setUrlInput(value)
  }

  function handleSubmit(event) {
    if (!urlInput){
      return
    }
    console.log(urlInput)

    try {
      const url = new URL(urlInput)
      const searchParams = new URLSearchParams(url.search)
      const ytid = searchParams.get('v')
      sendRequest(ytid)
      requestRandom()
      event.preventDefault()
    } catch (error) {
      console.log(error)
      alert("Not a valid Youtube video!")
    }
  }

  async function sendRequest(ytid){
    try {
      const response = await fetch(`http://127.0.0.1:5000/?ytid=${ytid}`)
      const jsonData = await response.json()
      setResponseData(jsonData)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  async function requestRandom()
  {
    try{
      const response = await fetch('http://127.0.0.1:5000/random')
      const jsonData = await response.json
      setRandomVideo(jsonData["ytid"])
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }
  // change this as you move the state for result up
  useEffect(() => {
    if (responseData.ytid || responseData.ytid === 0){
      setHasResult(true)
    } else {
      setHasResult(false)
    }
    
  }, [responseData])

  console.log(hasResult)

  return (
    <>
      <div className='parent'>
        <form onSubmit={handleSubmit}>
          <button className="searchbar--icon" type='submit'><SeachSvg/></button>
          <input className="searchbar--input" type="text" onChange={handleChange} value={urlInput}/>
        </form>
      </div>
      <div className='result' style={{visibility: hasResult ? "visible" : "hidden"}}>
        <p className='video-title'>{responseData.title}</p>
        <p><strong>{responseData.ytid === 0 ? "is not" : "is"}</strong>&nbsp;in AudioSet</p>
        <a 
        className='positive-link' 
        target='blank'
        href={`https://www.youtube.com/watch?v=${randomVideo}`}
        style={{display: responseData.ytid === 0 ? "block" : "none"}}>here's one that is.</a>
      </div>
    </>
  )
}

function App() {
  return (
    <div className='container'>
      <div className='content'>
          <div className='above'>
            <h1 className='title'>Is it in <a href='https://research.google.com/audioset/index.html' target='blank'>AudioSet?</a></h1>
            <p className='subtitle'>Enter a YouTube URL</p>
          </div>
        <Search/>
      </div>
    </div>
  );
}

export default App;
