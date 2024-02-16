import React, { useState } from "react";
import axios from 'axios'

const modelBaseUrl = process.env.REACT_APP_API_BASE_URL || "http://localhost:8080"

const Homepage = () => {

  const [messages,setMessages] = useState([{type: 'ai',message: 'Hello there ! How can I help you today ? ', date: new Date().toLocaleString()},])
  const [userInput, setUserInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function getInferenceFromUserInput(e){
    e.preventDefault();
    if(!userInput) return null
    setIsLoading(true);
    const userMessage = {type: 'user',message: userInput, date: new Date().toLocaleString()}
    setMessages((prev)=> [...prev,userMessage])
    const endPoint = `${modelBaseUrl}/get_rag_inference?prompt=${userInput}`
    
    setUserInput('')
    const response = await axios.get(endPoint)
    console.log(response.data.data)

    if(response.data.status !== '200'){
        alert('Internal Server Error')
    }else{
      const botMessage = {type: 'ai',message: response.data.data, date: new Date().toLocaleString()}
      setMessages((prev)=>[...prev, botMessage])
    }
    setIsLoading(false)
  }

  const renderChatMessages = messages.map((message)=>{
    if(message.type === 'ai'){
      return (<div className="col-start-1 col-end-8 p-3 rounded-lg">
      <div className="flex flex-row items-center">
        <div className="flex items-center justify-center h-10 w-10 rounded-full bg-gray-300 flex-shrink-0">
          AI 
        </div>
        <div className="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl">
          <div>
           {message.message}
          </div>
          <div className="absolute w-max-content text-xs bottom-0 right-0 -mb-5 mr-2 text-gray-500">
            {message.date}
          </div>
        </div>
      </div>
    </div>)
    }else{
      return  (<div className="col-start-6 col-end-13 p-3 rounded-lg">
      <div className="flex items-center justify-start flex-row-reverse">
        <div className="flex items-center justify-center h-10 w-10 rounded-full bg-indigo-500 flex-shrink-0">
         User
        </div>
        <div className="relative mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl">
          <div>
            {message.message}
          </div>
          <div className="absolute w-max-content text-xs bottom-0 right-0 -mb-5 mr-2 text-gray-500">
            {message.date}
          </div>
        </div>
      </div>
    </div>)
    }
  })

  return (
    <div className="flex h-screen antialiased text-gray-800">
      <div className="flex flex-row h-full w-full overflow-x-hidden">
        <div className="flex flex-col py-8 pl-6 pr-2 w-64 bg-white flex-shrink-0">
          <div className="flex flex-row items-center justify-center h-12 w-full">
            <div className="flex items-center justify-center rounded-2xl text-indigo-700 bg-indigo-100 h-10 w-10">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <div className="ml-2 font-bold text-2xl">Multi-hop RAG AI Chat</div>
          </div>
          <div className="flex flex-col mt-8">
            <div className="flex flex-row items-center justify-between text-xs">
              <span className="font-bold">Today's Chat History</span>
              <span className="flex items-center justify-center bg-gray-300 h-4 w-4 rounded-full">
               0
              </span>
            </div>
            <div className="flex flex-col space-y-1 mt-4 -mx-2 h-48 overflow-y-auto">
              <button className="flex flex-row items-center hover:bg-gray-100 rounded-xl p-2">
                <div className="text-sm font-semibold">AI Bot</div>
              </button>
            </div>
            <div className="flex flex-row items-center justify-between text-xs mt-6">
              <span className="font-bold">Yesterday Conversations</span>
              <span className="flex items-center justify-center bg-gray-300 h-4 w-4 rounded-full">
                7
              </span>
            </div>

          </div>
        </div>
        <div className="flex flex-col flex-auto h-full p-6">
          <div className="flex flex-col flex-auto flex-shrink-0 bg-gray-100 h-full p-4">
            <div className="flex flex-col h-full overflow-x-auto mb-4">
              <div className="flex flex-col h-full">
                <div className="grid grid-cols-12 gap-y-2">
                  {renderChatMessages}
                </div>
              </div>
            </div>
            <div className="flex flex-row items-center h-16 bg-white w-full px-4">
              <form onSubmit={getInferenceFromUserInput} class="flex flex-1 items-center">
              <div className="flex-grow">
                <div className="relative w-full">
                  <input
                    placeholder="Type here anything"
                    type="text"
                    value={userInput}
                    className="flex w-full border focus:outline-none focus:border-indigo-300 pl-4 h-10"
                    onChange={(e)=>setUserInput(e.target.value)}
                  />
                </div>
              </div>
              <div className="ml-4">
                <button className="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-1 flex-shrink-0"
                disabled={isLoading}
                type="submit"
                >
                  {isLoading ? 'Loading ...' : <><span>Send</span>
                  <span className="ml-2">
                    <svg
                      className="w-4 h-4 transform rotate-45 -mt-px"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                      />
                    </svg>
                  </span></>}
                  
                </button>
              </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
